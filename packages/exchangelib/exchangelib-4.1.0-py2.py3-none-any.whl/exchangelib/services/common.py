import abc
import logging
import traceback
from itertools import chain

from .. import errors
from ..credentials import IMPERSONATION, OAuth2Credentials
from ..errors import EWSWarning, TransportError, SOAPError, ErrorTimeoutExpired, ErrorBatchProcessingStopped, \
    ErrorQuotaExceeded, ErrorCannotDeleteObject, ErrorCreateItemAccessDenied, ErrorFolderNotFound, \
    ErrorNonExistentMailbox, ErrorMailboxStoreUnavailable, ErrorImpersonateUserDenied, ErrorInternalServerError, \
    ErrorInternalServerTransientError, ErrorNoRespondingCASInDestinationSite, ErrorImpersonationFailed, \
    ErrorMailboxMoveInProgress, ErrorAccessDenied, ErrorConnectionFailed, RateLimitError, ErrorServerBusy, \
    ErrorTooManyObjectsOpened, ErrorInvalidLicense, ErrorInvalidSchemaVersionForMailboxVersion, \
    ErrorInvalidServerVersion, ErrorItemNotFound, ErrorADUnavailable, ErrorInvalidChangeKey, \
    ErrorItemSave, ErrorInvalidIdMalformed, ErrorMessageSizeExceeded, UnauthorizedError, \
    ErrorCannotDeleteTaskOccurrence, ErrorMimeContentConversionFailed, ErrorRecurrenceHasNoOccurrence, \
    ErrorNoPublicFolderReplicaAvailable, MalformedResponseError, ErrorExceededConnectionCount, \
    SessionPoolMinSizeReached, ErrorIncorrectSchemaVersion, ErrorInvalidRequest, ErrorCorruptData, \
    ErrorCannotEmptyFolder, ErrorDeleteDistinguishedFolder, ErrorInvalidSubscription, ErrorInvalidWatermark
from ..properties import FieldURI, IndexedFieldURI, ExtendedFieldURI, ExceptionFieldURI, ItemId
from ..transport import wrap
from ..util import chunkify, create_element, add_xml_child, get_xml_attr, to_xml, post_ratelimited, \
    xml_to_str, set_xml_value, SOAPNS, TNS, MNS, ENS, ParseError
from ..version import API_VERSIONS, Version

log = logging.getLogger(__name__)

CHUNK_SIZE = 100  # A default chunk size for all services

KNOWN_EXCEPTIONS = (
    ErrorAccessDenied,
    ErrorADUnavailable,
    ErrorBatchProcessingStopped,
    ErrorCannotDeleteObject,
    ErrorCannotEmptyFolder,
    ErrorConnectionFailed,
    ErrorCreateItemAccessDenied,
    ErrorDeleteDistinguishedFolder,
    ErrorExceededConnectionCount,
    ErrorFolderNotFound,
    ErrorImpersonateUserDenied,
    ErrorImpersonationFailed,
    ErrorInternalServerError,
    ErrorInternalServerTransientError,
    ErrorInvalidChangeKey,
    ErrorInvalidLicense,
    ErrorInvalidSubscription,
    ErrorInvalidWatermark,
    ErrorItemNotFound,
    ErrorMailboxMoveInProgress,
    ErrorMailboxStoreUnavailable,
    ErrorNonExistentMailbox,
    ErrorNoPublicFolderReplicaAvailable,
    ErrorNoRespondingCASInDestinationSite,
    ErrorQuotaExceeded,
    ErrorTimeoutExpired,
    RateLimitError,
    UnauthorizedError,
)


class EWSService(metaclass=abc.ABCMeta):
    """Base class for all EWS services."""

    SERVICE_NAME = None  # The name of the SOAP service
    element_container_name = None  # The name of the XML element wrapping the collection of returned items
    paging_container_name = None  # The name of the element that contains paging information and the paged results
    returns_elements = True  # If False, the service does not return response elements, just the RsponseCode status
    # Return exception instance instead of raising exceptions for the following errors when contained in an element
    ERRORS_TO_CATCH_IN_RESPONSE = (
        EWSWarning, ErrorCannotDeleteObject, ErrorInvalidChangeKey, ErrorItemNotFound, ErrorItemSave,
        ErrorInvalidIdMalformed, ErrorMessageSizeExceeded, ErrorCannotDeleteTaskOccurrence,
        ErrorMimeContentConversionFailed, ErrorRecurrenceHasNoOccurrence, ErrorCorruptData
    )
    # Similarly, define the warnings we want to return unraised
    WARNINGS_TO_CATCH_IN_RESPONSE = ErrorBatchProcessingStopped
    # Define the warnings we want to ignore, to let response processing proceed
    WARNINGS_TO_IGNORE_IN_RESPONSE = ()
    # The exception type to raise when all attempted API versions failed
    NO_VALID_SERVER_VERSIONS = ErrorInvalidServerVersion
    # Controls whether the HTTP request should be streaming or fetch everything at once
    streaming = False
    # Marks the version from which the service was introduced
    supported_from = None
    # Marks services that support paging of requested items
    supports_paging = False
    # Marks services that need affinity to the backend server
    prefer_affinity = False

    def __init__(self, protocol, chunk_size=None, timeout=None):
        self.chunk_size = chunk_size or CHUNK_SIZE  # The number of items to send in a single request
        if not isinstance(self.chunk_size, int):
            raise ValueError("'chunk_size' %r must be an integer" % chunk_size)
        if self.chunk_size < 1:
            raise ValueError("'chunk_size' must be a positive number")
        if self.supported_from and protocol.version.build < self.supported_from:
            raise NotImplementedError(
                '%r is only supported on %r and later' % (self.SERVICE_NAME, self.supported_from.fullname())
            )
        self.protocol = protocol
        # Allow a service to override the default protocol timeout. Useful for streaming services
        self.timeout = timeout

    # The following two methods are the minimum required to be implemented by subclasses, but the name and number of
    # kwargs differs between services. Therefore, we cannot make these methods abstract.

    # @abc.abstractmethod
    # def call(self, **kwargs):
    #     """Defines the arguments required by the service. Arguments are basic Python types or EWSElement objects.
    #     Returns either XML objects or EWSElement objects.
    #     """"
    #     pass

    # @abc.abstractmethod
    # def get_payload(self, **kwargs):
    #     """Using the arguments from .call(), return the payload expected by the service, as an XML object. The XML
    #     object should consist of a SERVICE_NAME element and everything within that.
    #     """
    #     pass

    def get(self, expect_result=True, **kwargs):
        """Like .call(), but expects exactly one result from the server, or zero when expect_result=False, or either
        zero or one when expect_result=None. Returns either one object or None.

        :param expect_result: None, True, or False
        :param kwargs: Same as arguments for .call()
        :return: Same as .call(), but returns either None or exactly one item
        """
        res = list(self.call(**kwargs))
        if expect_result is None and not res:
            # Allow empty result
            return None
        if expect_result is False:
            if res:
                raise ValueError('Expected result length 0, but got %r' % res)
            return None
        if len(res) != 1:
            raise ValueError('Expected result length 1, but got %r' % res)
        if isinstance(res[0], Exception):
            raise res[0]
        return res[0]

    @property
    def _version_hint(self):
        # We may be here due to version guessing in Protocol.version, so we can't use the self.protocol.version property
        return self.protocol.config.version

    @_version_hint.setter
    def _version_hint(self, value):
        self.protocol.config.version = value

    def _extra_headers(self, session):
        headers = {}
        if self.prefer_affinity:
            headers['X-PreferServerAffinity'] = 'True'
        for cookie in session.cookies:
            if cookie.name == 'X-BackEndCookie':
                headers['X-BackEndOverrideCookie'] = cookie.value
        return headers

    @property
    def _account_to_impersonate(self):
        if isinstance(self.protocol.credentials, OAuth2Credentials):
            return self.protocol.credentials.identity
        return None

    @property
    def _timezone(self):
        return None

    def _response_generator(self, payload):
        """Send the payload to the server, and return the response.

        :param payload: payload as an XML object
        :return: the response, as XML objects
        """
        response = self._get_response_xml(payload=payload)
        if self.supports_paging:
            return (self._get_page(message) for message in response)
        return self._get_elements_in_response(response=response)

    def _chunked_get_elements(self, payload_func, items, **kwargs):
        """Yield elements in a response. Like ._get_elements(), but chop items into suitable chunks and send multiple
        requests.

        :param payload_func: A reference to .payload()
        :param items: An iterable of items (messages, folders, etc.) to process
        :param kwargs: Same as arguments for .call(), except for the 'items' argument
        :return: Same as ._get_elements()
        """
        for i, chunk in enumerate(chunkify(items, self.chunk_size), start=1):
            log.debug('Processing chunk %s containing %s items', i, len(chunk))
            yield from self._get_elements(payload=payload_func(chunk, **kwargs))

    def _get_elements(self, payload):
        """Send the payload to be sent and parsed. Handles and re-raise exceptions that are not meant to be returned
        to the caller as exception objects. Retry the request according to the retry policy.
        """
        while True:
            try:
                # Create a generator over the response elements so exceptions in response elements are also raised
                # here and can be handled.
                yield from self._response_generator(payload=payload)
                return
            except ErrorServerBusy as e:
                self._handle_backoff(e)
                continue
            except KNOWN_EXCEPTIONS:
                # These are known and understood, and don't require a backtrace.
                raise
            except (ErrorTooManyObjectsOpened, ErrorTimeoutExpired) as e:
                # ErrorTooManyObjectsOpened means there are too many connections to the Exchange database. This is very
                # often a symptom of sending too many requests.
                #
                # ErrorTimeoutExpired can be caused by a busy server, or by overly large requests. Start by lowering the
                # session count. This is done by downstream code.
                if isinstance(e, ErrorTimeoutExpired) and self.protocol.session_pool_size <= 1:
                    # We're already as low as we can go, so downstream cannot limit the session count to put less load
                    # on the server. We don't have a way of lowering the page size of requests from
                    # this part of the code yet. Let the user handle this.
                    raise e

                # Re-raise as an ErrorServerBusy with a default delay of 5 minutes
                raise ErrorServerBusy('Reraised from %s(%s)' % (e.__class__.__name__, e))
            except Exception:
                # This may run from a thread pool, which obfuscates the stack trace. Print trace immediately.
                account = self.account if isinstance(self, EWSAccountService) else None
                log.warning('Account %s: Exception in _get_elements: %s', account, traceback.format_exc(20))
                raise

    def _get_response_and_session(self, payload, api_version):
        """Send the actual HTTP request and get the response."""
        session = self.protocol.get_session()
        return post_ratelimited(
            protocol=self.protocol,
            session=session,
            url=self.protocol.service_endpoint,
            headers=self._extra_headers(session),
            data=wrap(
                content=payload,
                api_version=api_version,
                account_to_impersonate=self._account_to_impersonate,
                timezone=self._timezone,
            ),
            allow_redirects=False,
            stream=self.streaming,
            timeout=self.timeout or self.protocol.TIMEOUT,
        )

    @property
    def _api_versions_to_try(self):
        # Put the hint first in the list, and then all other versions except the hint, from newest to oldest
        return [self._version_hint.api_version] + [v for v in API_VERSIONS if v != self._version_hint.api_version]

    def _get_response_xml(self, payload, **parse_opts):
        """Send the payload to the server and return relevant elements from the result. Several things happen here:
          * The payload is wrapped in SOAP headers and sent to the server
          * The Exchange API version is negotiated and stored in the protocol object
          * Connection errors are handled and possibly reraised as ErrorServerBusy
          * SOAP errors are raised
          * EWS errors are raised, or passed on to the caller

        :param payload: The request payload, as an XML object
        :return: A generator of XML objects or None if the service does not return a result
        """
        # Microsoft really doesn't want to make our lives easy. The server may report one version in our initial version
        # guessing tango, but then the server may decide that any arbitrary legacy backend server may actually process
        # the request for an account. Prepare to handle version-related errors and set the server version per-account.
        log.debug('Calling service %s', self.SERVICE_NAME)
        for api_version in self._api_versions_to_try:
            log.debug('Trying API version %s', api_version)
            r, session = self._get_response_and_session(payload=payload, api_version=api_version)
            # TODO: We should only release the session when we have fully consumed the response, but in streaming mode
            #  that requires fully consuming the generator returned by _get_soap_messages. The caller may not always do
            #  that. Not doing so seems to not cause any trouble, though.
            self.protocol.release_session(session)
            if self.streaming:
                # Let 'requests' decode raw data automatically
                r.raw.decode_content = True
            try:
                header, body = self._get_soap_parts(response=r, **parse_opts)
            except Exception:
                r.close()  # Release memory
                raise
            # The body may contain error messages from Exchange, but we still want to collect version info
            if header is not None:
                self._update_api_version(api_version=api_version, header=header, **parse_opts)
            try:
                return self._get_soap_messages(body=body, **parse_opts)
            except (ErrorInvalidServerVersion, ErrorIncorrectSchemaVersion, ErrorInvalidRequest,
                    ErrorInvalidSchemaVersionForMailboxVersion):
                # The guessed server version is wrong. Try the next version
                log.debug('API version %s was invalid', api_version)
                continue
            except ErrorExceededConnectionCount as e:
                # This indicates that the connecting user has too many open TCP connections to the server. Decrease
                # our session pool size.
                try:
                    self.protocol.decrease_poolsize()
                    continue
                except SessionPoolMinSizeReached:
                    # We're already as low as we can go. Let the user handle this.
                    raise e
            finally:
                if not self.streaming:
                    # In streaming mode, we may not have accessed the raw stream yet. Caller must handle this.
                    r.close()  # Release memory

        raise self.NO_VALID_SERVER_VERSIONS('Tried versions %s but all were invalid' % self._api_versions_to_try)

    def _handle_backoff(self, e):
        """Take a request from the server to back off and checks the retry policy for what to do. Re-raise the
        exception if conditions are not met.

        :param e: An ErrorServerBusy instance
        :return:
        """
        log.debug('Got ErrorServerBusy (back off %s seconds)', e.back_off)
        # ErrorServerBusy is very often a symptom of sending too many requests. Scale back connections if possible.
        try:
            self.protocol.decrease_poolsize()
        except SessionPoolMinSizeReached:
            pass
        if self.protocol.retry_policy.fail_fast:
            raise e
        self.protocol.retry_policy.back_off(e.back_off)
        # We'll warn about this later if we actually need to sleep

    def _update_api_version(self, api_version, header, **parse_opts):
        """Parse the server version contained in SOAP headers and update the version hint stored by the caller, if
        necessary.
        """
        try:
            head_version = Version.from_soap_header(requested_api_version=api_version, header=header)
        except TransportError as te:
            log.debug('Failed to update version info (%s)', te)
            return
        if self._version_hint == head_version:
            # Nothing to do
            return
        log.debug('Found new version (%s -> %s)', self._version_hint, head_version)
        # The api_version that worked was different than our hint, or we never got a build version. Store the working
        # version.
        self._version_hint = head_version

    @classmethod
    def _response_tag(cls):
        """Return the name of the element containing the service response."""
        return '{%s}%sResponse' % (MNS, cls.SERVICE_NAME)

    @staticmethod
    def _response_messages_tag():
        """Return the name of the element containing service response messages."""
        return '{%s}ResponseMessages' % MNS

    @classmethod
    def _response_message_tag(cls):
        """Return the name of the element of a single response message."""
        return '{%s}%sResponseMessage' % (MNS, cls.SERVICE_NAME)

    @classmethod
    def _get_soap_parts(cls, response, **parse_opts):
        """Split the SOAP response into its headers an body elements."""
        try:
            root = to_xml(response.iter_content())
        except ParseError as e:
            raise SOAPError('Bad SOAP response: %s' % e)
        header = root.find('{%s}Header' % SOAPNS)
        if header is None:
            # This is normal when the response contains SOAP-level errors
            log.debug('No header in XML response')
        body = root.find('{%s}Body' % SOAPNS)
        if body is None:
            raise MalformedResponseError('No Body element in SOAP response')
        return header, body

    def _get_soap_messages(self, body, **parse_opts):
        """Return the elements in the response containing the response messages. Raises any SOAP exceptions."""
        response = body.find(self._response_tag())
        if response is None:
            fault = body.find('{%s}Fault' % SOAPNS)
            if fault is None:
                raise SOAPError(
                    'Unknown SOAP response (expected %s or Fault): %s' % (self._response_tag(), xml_to_str(body))
                )
            self._raise_soap_errors(fault=fault)  # Will throw SOAPError or custom EWS error
        response_messages = response.find(self._response_messages_tag())
        if response_messages is None:
            # Result isn't delivered in a list of FooResponseMessages, but directly in the FooResponse. Consumers expect
            # a list, so return a list
            return [response]
        return response_messages.findall(self._response_message_tag())

    @classmethod
    def _raise_soap_errors(cls, fault):
        """Parse error messages contained in SOAP headers and raise as exceptions defined in this package."""
        # Fault: See http://www.w3.org/TR/2000/NOTE-SOAP-20000508/#_Toc478383507
        faultcode = get_xml_attr(fault, 'faultcode')
        faultstring = get_xml_attr(fault, 'faultstring')
        faultactor = get_xml_attr(fault, 'faultactor')
        detail = fault.find('detail')
        if detail is not None:
            code, msg = None, ''
            if detail.find('{%s}ResponseCode' % ENS) is not None:
                code = get_xml_attr(detail, '{%s}ResponseCode' % ENS).strip()
            if detail.find('{%s}Message' % ENS) is not None:
                msg = get_xml_attr(detail, '{%s}Message' % ENS).strip()
            msg_xml = detail.find('{%s}MessageXml' % TNS)  # Crazy. Here, it's in the TNS namespace
            if code == 'ErrorServerBusy':
                back_off = None
                try:
                    value = msg_xml.find('{%s}Value' % TNS)
                    if value.get('Name') == 'BackOffMilliseconds':
                        back_off = int(value.text) / 1000.0  # Convert to seconds
                except (TypeError, AttributeError):
                    pass
                raise ErrorServerBusy(msg, back_off=back_off)
            if code == 'ErrorSchemaValidation' and msg_xml is not None:
                violation = get_xml_attr(msg_xml, '{%s}Violation' % TNS)
                if violation is not None:
                    msg = '%s %s' % (msg, violation)
            try:
                raise vars(errors)[code](msg)
            except KeyError:
                detail = '%s: code: %s msg: %s (%s)' % (cls.SERVICE_NAME, code, msg, xml_to_str(detail))
        try:
            raise vars(errors)[faultcode](faultstring)
        except KeyError:
            pass
        raise SOAPError('SOAP error code: %s string: %s actor: %s detail: %s' % (
            faultcode, faultstring, faultactor, detail))

    def _get_element_container(self, message, name=None):
        """Return the XML element in a response element that contains the elements we want the service to return. For
        example, in a GetFolder response, 'message' is the GetFolderResponseMessage element, and we return the 'Folders'
        element:

        <m:GetFolderResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Folders>
            <t:Folder>
              <t:FolderId Id="AQApA=" ChangeKey="AQAAAB" />
              [...]
            </t:Folder>
          </m:Folders>
        </m:GetFolderResponseMessage>

        Some service responses don't have a containing element for the returned elements ('name' is None). In
        that case, we return the 'SomeServiceResponseMessage' element.

        If the response contains a warning or an error message, we raise the relevant exception, unless the error class
        is contained in WARNINGS_TO_CATCH_IN_RESPONSE or ERRORS_TO_CATCH_IN_RESPONSE, in which case we return the
        exception instance.
        """
        # ResponseClass is an XML attribute of various SomeServiceResponseMessage elements: Possible values are:
        # Success, Warning, Error. See e.g.
        # https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/finditemresponsemessage
        response_class = message.get('ResponseClass')
        # ResponseCode, MessageText: See
        # https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/responsecode
        response_code = get_xml_attr(message, '{%s}ResponseCode' % MNS)
        if response_class == 'Success' and response_code == 'NoError':
            if not name:
                return message
            container = message.find(name)
            if container is None:
                raise MalformedResponseError('No %s elements in ResponseMessage (%s)' % (name, xml_to_str(message)))
            return container
        if response_code == 'NoError':
            return True
        # Raise any non-acceptable errors in the container, or return the container or the acceptable exception instance
        msg_text = get_xml_attr(message, '{%s}MessageText' % MNS)
        msg_xml = message.find('{%s}MessageXml' % MNS)
        if response_class == 'Warning':
            try:
                raise self._get_exception(code=response_code, text=msg_text, msg_xml=msg_xml)
            except self.WARNINGS_TO_CATCH_IN_RESPONSE as e:
                return e
            except self.WARNINGS_TO_IGNORE_IN_RESPONSE as e:
                log.warning(str(e))
                container = message.find(name)
                if container is None:
                    raise MalformedResponseError('No %s elements in ResponseMessage (%s)' % (name, xml_to_str(message)))
                return container
        # rspclass == 'Error', or 'Success' and not 'NoError'
        try:
            raise self._get_exception(code=response_code, text=msg_text, msg_xml=msg_xml)
        except self.ERRORS_TO_CATCH_IN_RESPONSE as e:
            return e

    @staticmethod
    def _get_exception(code, text, msg_xml):
        """Parse error messages contained in EWS responses and raise as exceptions defined in this package."""
        if not code:
            return TransportError('Empty ResponseCode in ResponseMessage (MessageText: %s, MessageXml: %s)' % (
                text, msg_xml))
        if msg_xml is not None:
            # If this is an ErrorInvalidPropertyRequest error, the xml may contain a specific FieldURI
            for elem_cls in (FieldURI, IndexedFieldURI, ExtendedFieldURI, ExceptionFieldURI):
                elem = msg_xml.find(elem_cls.response_tag())
                if elem is not None:
                    field_uri = elem_cls.from_xml(elem, account=None)
                    text += ' (field: %s)' % field_uri
                    break

            # If this is an ErrorInvalidValueForProperty error, the xml may contain the name and value of the property
            if code == 'ErrorInvalidValueForProperty':
                msg_parts = {}
                for elem in msg_xml.findall('{%s}Value' % TNS):
                    key, val = elem.get('Name'), elem.text
                    if key:
                        msg_parts[key] = val
                if msg_parts:
                    text += ' (%s)' % ', '.join('%s: %s' % (k, v) for k, v in msg_parts.items())

            # If this is an ErrorInternalServerError error, the xml may contain a more specific error code
            inner_code, inner_text = None, None
            for value_elem in msg_xml.findall('{%s}Value' % TNS):
                name = value_elem.get('Name')
                if name == 'InnerErrorResponseCode':
                    inner_code = value_elem.text
                elif name == 'InnerErrorMessageText':
                    inner_text = value_elem.text
            if inner_code:
                try:
                    # Raise the error as the inner error code
                    return vars(errors)[inner_code]('%s (raised from: %s(%r))' % (inner_text, code, text))
                except KeyError:
                    # Inner code is unknown to us. Just append to the original text
                    text += ' (inner error: %s(%r))' % (inner_code, inner_text)
        try:
            # Raise the error corresponding to the ResponseCode
            return vars(errors)[code](text)
        except KeyError:
            # Should not happen
            return TransportError('Unknown ResponseCode in ResponseMessage: %s (MessageText: %s, MessageXml: %s)' % (
                    code, text, msg_xml))

    def _get_elements_in_response(self, response):
        """Take a list of 'SomeServiceResponseMessage' elements and return the elements in each response message that
        we want the service to return. With e.g. 'CreateItem', we get a list of 'CreateItemResponseMessage' elements
        and return the 'Message' elements.

        <m:CreateItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:Message>
              <t:ItemId Id="AQApA=" ChangeKey="AQAAAB"/>
            </t:Message>
          </m:Items>
        </m:CreateItemResponseMessage>
        <m:CreateItemResponseMessage ResponseClass="Success">
          <m:ResponseCode>NoError</m:ResponseCode>
          <m:Items>
            <t:Message>
              <t:ItemId Id="AQApB=" ChangeKey="AQAAAC"/>
            </t:Message>
          </m:Items>
        </m:CreateItemResponseMessage>

        :param response: a list of 'SomeServiceResponseMessage' XML objects
        :return: a generator of items as returned by '_get_elements_in_container()
        """
        for msg in response:
            container_or_exc = self._get_element_container(message=msg, name=self.element_container_name)
            if isinstance(container_or_exc, (bool, Exception)):
                yield container_or_exc
            else:
                for c in self._get_elements_in_container(container=container_or_exc):
                    yield c

    @classmethod
    def _get_elements_in_container(cls, container):
        """Return a list of response elements from an XML response element container. With e.g.
        'CreateItem', 'Items' is the container element and we return the 'Message' child elements:

          <m:Items>
            <t:Message>
              <t:ItemId Id="AQApA=" ChangeKey="AQAAAB"/>
            </t:Message>
          </m:Items>

        If the service does not return response elements, return True to indicate the status. Errors have already been
        raised.
        """
        if cls.returns_elements:
            return list(container)
        return [True]

    def _get_elems_from_page(self, elem, max_items, total_item_count):
        container = elem.find(self.element_container_name)
        if container is None:
            raise MalformedResponseError('No %s elements in ResponseMessage (%s)' % (
                self.element_container_name, xml_to_str(elem)))
        for e in self._get_elements_in_container(container=container):
            if max_items and total_item_count >= max_items:
                # No need to continue. Break out of elements loop
                log.debug("'max_items' count reached (elements)")
                break
            yield e

    def _get_pages(self, payload_func, kwargs, expected_message_count):
        """Request a page, or a list of pages if multiple collections are pages in a single request. Return each
        page.
        """
        payload = payload_func(**kwargs)
        page_elems = list(self._get_elements(payload=payload))
        if len(page_elems) != expected_message_count:
            raise MalformedResponseError(
                "Expected %s items in 'response', got %s" % (expected_message_count, len(page_elems))
            )
        return page_elems

    @staticmethod
    def _get_next_offset(paging_infos):
        next_offsets = {p['next_offset'] for p in paging_infos if p['next_offset'] is not None}
        if not next_offsets:
            # Paging is done for all messages
            return None
        # We cannot guarantee that all messages that have a next_offset also have the *same* next_offset. This is
        # because the collections that we are iterating may change while iterating. We'll do our best but we cannot
        # guarantee 100% consistency when large collections are simultaneously being changed on the server.
        #
        # It's not possible to supply a per-folder offset when iterating multiple folders, so we'll just have to
        # choose something that is most likely to work. Select the lowest of all the values to at least make sure
        # we don't miss any items, although we may then get duplicates ¯\_(ツ)_/¯
        if len(next_offsets) > 1:
            log.warning('Inconsistent next_offset values: %r. Using lowest value', next_offsets)
        return min(next_offsets)

    def _paged_call(self, payload_func, max_items, expected_message_count, **kwargs):
        """Call a service that supports paging requests. Return a generator over all response items. Keeps track of
        all paging-related counters.
        """
        paging_infos = [dict(item_count=0, next_offset=None) for _ in range(expected_message_count)]
        common_next_offset = kwargs['offset']
        total_item_count = 0
        while True:
            log.debug('Getting page at offset %s (max_items %s)', common_next_offset, max_items)
            kwargs['offset'] = common_next_offset
            pages = self._get_pages(payload_func, kwargs, expected_message_count)
            for (page, next_offset), paging_info in zip(pages, paging_infos):
                paging_info['next_offset'] = next_offset
                if isinstance(page, Exception):
                    yield page
                    continue
                if page is not None:
                    for elem in self._get_elems_from_page(page, max_items, total_item_count):
                        paging_info['item_count'] += 1
                        total_item_count += 1
                        yield elem
                    if max_items and total_item_count >= max_items:
                        # No need to continue. Break out of inner loop
                        log.debug("'max_items' count reached (inner)")
                        break
                if not paging_info['next_offset']:
                    # Paging is done for this message
                    continue
                # Check sanity of paging offsets, but don't fail. When we are iterating huge collections that take a
                # long time to complete, the collection may change while we are iterating. This can affect the
                # 'next_offset' value and make it inconsistent with the number of already collected items.
                # We may have a mismatch if we stopped early due to reaching 'max_items'.
                if paging_info['next_offset'] != paging_info['item_count'] and (
                    not max_items or total_item_count < max_items
                ):
                    log.warning('Unexpected next offset: %s -> %s. Maybe the server-side collection has changed?',
                                paging_info['item_count'], paging_info['next_offset'])
            # Also break out of outer loop
            if max_items and total_item_count >= max_items:
                log.debug("'max_items' count reached (outer)")
                break
            common_next_offset = self._get_next_offset(paging_infos)
            if common_next_offset is None:
                # Paging is done for all messages
                break

    @staticmethod
    def _get_paging_values(elem):
        """Read paging information from the paging container element."""
        is_last_page = elem.get('IncludesLastItemInRange').lower() in ('true', '0')
        offset = elem.get('IndexedPagingOffset')
        if offset is None and not is_last_page:
            log.debug("Not last page in range, but Exchange didn't send a page offset. Assuming first page")
            offset = '1'
        next_offset = None if is_last_page else int(offset)
        item_count = int(elem.get('TotalItemsInView'))
        if not item_count and next_offset is not None:
            raise ValueError("Expected empty 'next_offset' when 'item_count' is 0")
        log.debug('Got page with next offset %s (last_page %s)', next_offset, is_last_page)
        return item_count, next_offset

    def _get_page(self, message):
        """Get a single page from a request message, and return the container and next offset."""
        paging_elem = self._get_element_container(message=message, name=self.paging_container_name)
        if isinstance(paging_elem, Exception):
            return paging_elem, None
        item_count, next_offset = self._get_paging_values(paging_elem)
        if not item_count:
            paging_elem = None
        return paging_elem, next_offset


class EWSAccountService(EWSService, metaclass=abc.ABCMeta):
    """Base class for services that act on items concerning a single Mailbox on the server."""

    NO_VALID_SERVER_VERSIONS = ErrorInvalidSchemaVersionForMailboxVersion

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        kwargs['protocol'] = self.account.protocol
        super().__init__(*args, **kwargs)

    @property
    def _version_hint(self):
        return self.account.version

    @_version_hint.setter
    def _version_hint(self, value):
        self.account.version = value

    def _extra_headers(self, *args, **kwargs):
        headers = super()._extra_headers(*args, **kwargs)
        # See
        # https://blogs.msdn.microsoft.com/webdav_101/2015/05/11/best-practices-ews-authentication-and-access-issues/
        headers['X-AnchorMailbox'] = self.account.primary_smtp_address
        return headers

    @property
    def _account_to_impersonate(self):
        if self.account.access_type == IMPERSONATION:
            return self.account.identity
        return None

    @property
    def _timezone(self):
        return self.account.default_timezone


def to_item_id(item, item_cls, version):
    # Coerce a tuple, dict or object to an 'item_cls' instance. Used to create [Parent][Item|Folder]Id instances from a
    # variety of input.
    if isinstance(item, item_cls):
        # Allow any subclass of item_cls, e.g. OccurrenceItemId when ItemId is passed
        return item
    from ..folders import BaseFolder
    from ..items import BaseItem
    if isinstance(item, (BaseFolder, BaseItem)):
        return item.to_id_xml(version=version)
    if isinstance(item, (tuple, list)):
        return item_cls(*item)
    if isinstance(item, dict):
        return item_cls(**item)
    return item_cls(item.id, item.changekey)


def create_shape_element(tag, shape, additional_fields, version):
    shape_elem = create_element(tag)
    add_xml_child(shape_elem, 't:BaseShape', shape)
    if additional_fields:
        additional_properties = create_element('t:AdditionalProperties')
        expanded_fields = chain(*(f.expand(version=version) for f in additional_fields))
        set_xml_value(additional_properties, sorted(expanded_fields, key=lambda f: f.path), version=version)
        shape_elem.append(additional_properties)
    return shape_elem


def create_folder_ids_element(tag, folders, version):
    from ..folders import FolderId
    folder_ids = create_element(tag)
    for folder in folders:
        if not isinstance(folder, FolderId):
            folder = to_item_id(folder, FolderId, version=version)
        set_xml_value(folder_ids, folder, version=version)
    if not len(folder_ids):
        raise ValueError('"folders" must not be empty')
    return folder_ids


def create_item_ids_element(items, version, tag='m:ItemIds'):
    item_ids = create_element(tag)
    for item in items:
        set_xml_value(item_ids, to_item_id(item, ItemId, version=version), version=version)
    if not len(item_ids):
        raise ValueError('"items" must not be empty')
    return item_ids


def create_attachment_ids_element(items, version):
    from ..attachments import AttachmentId
    attachment_ids = create_element('m:AttachmentIds')
    for item in items:
        attachment_id = item if isinstance(item, AttachmentId) else AttachmentId(id=item)
        set_xml_value(attachment_ids, attachment_id, version=version)
    if not len(attachment_ids):
        raise ValueError('"items" must not be empty')
    return attachment_ids


def parse_folder_elem(elem, folder, account):
    from ..folders import BaseFolder, Folder, DistinguishedFolderId, RootOfHierarchy
    if isinstance(elem, Exception):
        return elem
    if isinstance(folder, RootOfHierarchy):
        f = folder.from_xml(elem=elem, account=folder.account)
    elif isinstance(folder, Folder):
        f = folder.from_xml_with_root(elem=elem, root=folder.root)
    elif isinstance(folder, DistinguishedFolderId):
        # We don't know the root, so assume account.root.
        folder_cls = None
        for cls in account.root.WELLKNOWN_FOLDERS:
            if cls.DISTINGUISHED_FOLDER_ID == folder.id:
                folder_cls = cls
                break
        if not folder_cls:
            raise ValueError('Unknown distinguished folder ID: %s' % folder.id)
        f = folder_cls.from_xml_with_root(elem=elem, root=account.root)
    else:
        # 'folder' is a generic FolderId instance. We don't know the root so assume account.root.
        f = Folder.from_xml_with_root(elem=elem, root=account.root)
    if isinstance(folder, DistinguishedFolderId):
        f.is_distinguished = True
    elif isinstance(folder, BaseFolder) and folder.is_distinguished:
        f.is_distinguished = True
    return f
