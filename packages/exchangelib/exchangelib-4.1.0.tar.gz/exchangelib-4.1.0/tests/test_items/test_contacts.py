import datetime
try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

from exchangelib.errors import ErrorInvalidIdMalformed
from exchangelib.folders import Contacts, FolderCollection
from exchangelib.indexed_properties import EmailAddress, PhysicalAddress
from exchangelib.items import Contact, DistributionList, Persona
from exchangelib.properties import Mailbox, Member, Attribution, SourceId, FolderId, StringAttributedValue, \
    PhoneNumberAttributedValue, PersonaPhoneNumberTypeValue
from exchangelib.queryset import QuerySet
from exchangelib.services import GetPersona

from ..common import get_random_string, get_random_email, MockResponse
from .test_basics import CommonItemTest


class ContactsTest(CommonItemTest):
    TEST_FOLDER = 'contacts'
    FOLDER_CLASS = Contacts
    ITEM_CLASS = Contact

    def test_order_by_on_indexed_field(self):
        # Test order_by() on IndexedField (simple and multi-subfield). Only Contact items have these
        test_items = []
        label = self.random_val(EmailAddress.get_field_by_fieldname('label'))
        for i in range(4):
            item = self.get_test_item()
            item.email_addresses = [EmailAddress(email='%s@foo.com' % i, label=label)]
            test_items.append(item)
        self.test_folder.bulk_create(items=test_items)
        qs = QuerySet(
            folder_collection=FolderCollection(account=self.account, folders=[self.test_folder])
        ).filter(categories__contains=self.categories)
        self.assertEqual(
            [i[0].email for i in qs.order_by('email_addresses__%s' % label)
                .values_list('email_addresses', flat=True)],
            ['0@foo.com', '1@foo.com', '2@foo.com', '3@foo.com']
        )
        self.assertEqual(
            [i[0].email for i in qs.order_by('-email_addresses__%s' % label)
                .values_list('email_addresses', flat=True)],
            ['3@foo.com', '2@foo.com', '1@foo.com', '0@foo.com']
        )
        self.bulk_delete(qs)

        test_items = []
        label = self.random_val(PhysicalAddress.get_field_by_fieldname('label'))
        for i in range(4):
            item = self.get_test_item()
            item.physical_addresses = [PhysicalAddress(street='Elm St %s' % i, label=label)]
            test_items.append(item)
        self.test_folder.bulk_create(items=test_items)
        qs = QuerySet(
            folder_collection=FolderCollection(account=self.account, folders=[self.test_folder])
        ).filter(categories__contains=self.categories)
        self.assertEqual(
            [i[0].street for i in qs.order_by('physical_addresses__%s__street' % label)
                .values_list('physical_addresses', flat=True)],
            ['Elm St 0', 'Elm St 1', 'Elm St 2', 'Elm St 3']
        )
        self.assertEqual(
            [i[0].street for i in qs.order_by('-physical_addresses__%s__street' % label)
                .values_list('physical_addresses', flat=True)],
            ['Elm St 3', 'Elm St 2', 'Elm St 1', 'Elm St 0']
        )
        self.bulk_delete(qs)

    def test_order_by_failure(self):
        # Test error handling on indexed properties with labels and subfields
        qs = QuerySet(
            folder_collection=FolderCollection(account=self.account, folders=[self.test_folder])
        ).filter(categories__contains=self.categories)
        with self.assertRaises(ValueError):
            qs.order_by('email_addresses')  # Must have label
        with self.assertRaises(ValueError):
            qs.order_by('email_addresses__FOO')  # Must have a valid label
        with self.assertRaises(ValueError):
            qs.order_by('email_addresses__EmailAddress1__FOO')  # Must not have a subfield
        with self.assertRaises(ValueError):
            qs.order_by('physical_addresses__Business')  # Must have a subfield
        with self.assertRaises(ValueError):
            qs.order_by('physical_addresses__Business__FOO')  # Must have a valid subfield

    def test_distribution_lists(self):
        dl = DistributionList(folder=self.test_folder, display_name=get_random_string(255), categories=self.categories)
        dl.save()
        new_dl = self.test_folder.get(categories__contains=dl.categories)
        self.assertEqual(new_dl.display_name, dl.display_name)
        self.assertEqual(new_dl.members, None)
        dl.refresh()

        # We set mailbox_type to OneOff because otherwise the email address must be an actual account
        dl.members = {
            Member(mailbox=Mailbox(email_address=get_random_email(), mailbox_type='OneOff')) for _ in range(4)
        }
        dl.save()
        new_dl = self.test_folder.get(categories__contains=dl.categories)
        self.assertEqual({m.mailbox.email_address for m in new_dl.members}, dl.members)

        dl.delete()

    def test_find_people(self):
        # The test server may not have any contacts. Just test that the FindPeople and GetPersona services work.
        self.assertGreaterEqual(len(list(self.test_folder.people())), 0)
        self.assertGreaterEqual(
            len(list(
                self.test_folder.people().only('display_name').filter(display_name='john').order_by('display_name')
            )),
            0
        )

    def test_get_persona(self):
        ws = GetPersona(account=self.account)
        xml = b'''\
<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <m:GetPersonaResponseMessage ResponseClass="Success"
            xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
            xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
         <m:ResponseCode>NoError</m:ResponseCode>
         <m:Persona>
            <t:PersonaId Id="AAQkADEzAQAKtOtR="/>
            <t:PersonaType>Person</t:PersonaType>
            <t:CreationTime>2012-06-01T17:00:34Z</t:CreationTime>
            <t:DisplayName>Brian Johnson</t:DisplayName>
            <t:RelevanceScore>4255550110</t:RelevanceScore>
            <t:Attributions>
               <t:Attribution>
                  <t:Id>0</t:Id>
                  <t:SourceId Id="AAMkA =" ChangeKey="EQAAABY+"/>
                  <t:DisplayName>Outlook</t:DisplayName>
                  <t:IsWritable>true</t:IsWritable>
                  <t:IsQuickContact>false</t:IsQuickContact>
                  <t:IsHidden>false</t:IsHidden>
                  <t:FolderId Id="AAMkA=" ChangeKey="AQAAAA=="/>
               </t:Attribution>
            </t:Attributions>
            <t:DisplayNames>
               <t:StringAttributedValue>
                  <t:Value>Brian Johnson</t:Value>
                  <t:Attributions>
                     <t:Attribution>2</t:Attribution>
                     <t:Attribution>3</t:Attribution>
                  </t:Attributions>
               </t:StringAttributedValue>
            </t:DisplayNames>
            <t:MobilePhones>
               <t:PhoneNumberAttributedValue>
                  <t:Value>
                     <t:Number>(425)555-0110</t:Number>
                     <t:Type>Mobile</t:Type>
                  </t:Value>
                  <t:Attributions>
                     <t:Attribution>0</t:Attribution>
                  </t:Attributions>
               </t:PhoneNumberAttributedValue>
               <t:PhoneNumberAttributedValue>
                  <t:Value>
                     <t:Number>(425)555-0111</t:Number>
                     <t:Type>Mobile</t:Type>
                  </t:Value>
                  <t:Attributions>
                     <t:Attribution>1</t:Attribution>
                  </t:Attributions>
               </t:PhoneNumberAttributedValue>
            </t:MobilePhones>
         </m:Persona>
      </m:GetPersonaResponseMessage>
   </s:Body>
</s:Envelope>'''
        _, body = ws._get_soap_parts(response=MockResponse(xml))
        res = ws._get_elements_in_response(response=ws._get_soap_messages(body=body))
        personas = [Persona.from_xml(elem=elem, account=self.account) for elem in res]
        self.assertEqual(len(personas), 1)
        persona = personas[0]
        self.assertEqual(persona.id, 'AAQkADEzAQAKtOtR=')
        self.assertEqual(persona.persona_type, 'Person')
        self.assertEqual(
            persona.creation_time, datetime.datetime(2012, 6, 1, 17, 0, 34, tzinfo=zoneinfo.ZoneInfo('UTC'))
        )
        self.assertEqual(persona.display_name, 'Brian Johnson')
        self.assertEqual(persona.relevance_score, '4255550110')
        self.assertEqual(persona.attributions[0], Attribution(
            ID=None,
            _id=SourceId(id='AAMkA =', changekey='EQAAABY+'),
            display_name='Outlook',
            is_writable=True,
            is_quick_contact=False,
            is_hidden=False,
            folder_id=FolderId(id='AAMkA=', changekey='AQAAAA==')
        ))
        self.assertEqual(persona.display_names, [
            StringAttributedValue(value='Brian Johnson', attributions=['2', '3']),
        ])
        self.assertEqual(persona.mobile_phones, [
            PhoneNumberAttributedValue(
                value=PersonaPhoneNumberTypeValue(number='(425)555-0110', type='Mobile'),
                attributions=['0'],
            ),
            PhoneNumberAttributedValue(
                value=PersonaPhoneNumberTypeValue(number='(425)555-0111', type='Mobile'),
                attributions=['1'],
            )
        ])

    def test_get_persona_failure(self):
        # The test server may not have any personas. Just test that the service response with something we can parse
        persona = Persona(id='AAA=', changekey='xxx')
        try:
            GetPersona(account=self.account).call(persona=persona)
        except ErrorInvalidIdMalformed:
            pass
