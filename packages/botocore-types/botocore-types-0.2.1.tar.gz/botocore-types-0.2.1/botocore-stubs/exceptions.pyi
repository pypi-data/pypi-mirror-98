from typing import Any, Dict, Optional

import requests
from requests.packages.urllib3 import exceptions

_ErrorResponseDict = Dict[str, Any]

class BotoCoreError(Exception):
    fmt: str
    kwargs: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...

class DataNotFoundError(BotoCoreError):
    fmt: str

class UnknownServiceError(DataNotFoundError):
    fmt: str

class ApiVersionNotFoundError(BotoCoreError):
    fmt: str

class HTTPClientError(BotoCoreError):
    fmt: str
    request: Any
    response: Any
    def __init__(
        self, request: Optional[Any] = ..., response: Optional[Any] = ..., **kwargs: Any
    ) -> None: ...

class ConnectionError(BotoCoreError):
    fmt: str

class InvalidIMDSEndpointError(BotoCoreError):
    fmt: str

class EndpointConnectionError(ConnectionError):
    fmt: str

class SSLError(ConnectionError, requests.exceptions.SSLError):
    fmt: str

class ConnectionClosedError(HTTPClientError):
    fmt: str

class ReadTimeoutError(
    HTTPClientError, requests.exceptions.ReadTimeout, exceptions.ReadTimeoutError
):
    fmt: str

class ConnectTimeoutError(ConnectionError, requests.exceptions.ConnectTimeout):
    fmt: str

class ProxyConnectionError(ConnectionError, requests.exceptions.ProxyError):
    fmt: str

class NoCredentialsError(BotoCoreError):
    fmt: str

class PartialCredentialsError(BotoCoreError):
    fmt: str

class CredentialRetrievalError(BotoCoreError):
    fmt: str

class UnknownSignatureVersionError(BotoCoreError):
    fmt: str

class ServiceNotInRegionError(BotoCoreError):
    fmt: str

class BaseEndpointResolverError(BotoCoreError): ...

class NoRegionError(BaseEndpointResolverError):
    fmt: str

class UnknownEndpointError(BaseEndpointResolverError, ValueError):
    fmt: str

class ProfileNotFound(BotoCoreError):
    fmt: str

class ConfigParseError(BotoCoreError):
    fmt: str

class ConfigNotFound(BotoCoreError):
    fmt: str

class MissingParametersError(BotoCoreError):
    fmt: str

class ValidationError(BotoCoreError):
    fmt: str

class ParamValidationError(BotoCoreError):
    fmt: str

class UnknownKeyError(ValidationError):
    fmt: str

class RangeError(ValidationError):
    fmt: str

class UnknownParameterError(ValidationError):
    fmt: str

class InvalidRegionError(ValidationError, ValueError):
    fmt: str

class AliasConflictParameterError(ValidationError):
    fmt: str

class UnknownServiceStyle(BotoCoreError):
    fmt: str

class PaginationError(BotoCoreError):
    fmt: str

class OperationNotPageableError(BotoCoreError):
    fmt: str

class ChecksumError(BotoCoreError):
    fmt: str

class UnseekableStreamError(BotoCoreError):
    fmt: str

class WaiterError(BotoCoreError):
    fmt: str
    last_response: Any = ...
    def __init__(self, name: Any, reason: Any, last_response: Any) -> None: ...

class IncompleteReadError(BotoCoreError):
    fmt: str

class InvalidExpressionError(BotoCoreError):
    fmt: str

class UnknownCredentialError(BotoCoreError):
    fmt: str

class WaiterConfigError(BotoCoreError):
    fmt: str

class UnknownClientMethodError(BotoCoreError):
    fmt: str

class UnsupportedSignatureVersionError(BotoCoreError):
    fmt: str

class ClientError(Exception):
    MSG_TEMPLATE: str
    response: _ErrorResponseDict
    operation_name: str
    def __init__(
        self, error_response: _ErrorResponseDict, operation_name: str
    ) -> None: ...

class EventStreamError(ClientError): ...
class UnsupportedTLSVersionWarning(Warning): ...
class ImminentRemovalWarning(Warning): ...

class InvalidDNSNameError(BotoCoreError):
    fmt: str

class InvalidS3AddressingStyleError(BotoCoreError):
    fmt: str

class UnsupportedS3ArnError(BotoCoreError):
    fmt: str

class UnsupportedS3ControlArnError(BotoCoreError):
    fmt: str

class InvalidHostLabelError(BotoCoreError):
    fmt: str

class UnsupportedOutpostResourceError(BotoCoreError):
    fmt: str

class UnsupportedS3AccesspointConfigurationError(BotoCoreError):
    fmt: str

class InvalidEndpointDiscoveryConfigurationError(BotoCoreError):
    fmt: str

class UnsupportedS3ControlConfigurationError(BotoCoreError):
    fmt: str

class InvalidRetryConfigurationError(BotoCoreError):
    fmt: str

class InvalidMaxRetryAttemptsError(InvalidRetryConfigurationError):
    fmt: str

class InvalidRetryModeError(InvalidRetryConfigurationError):
    fmt: str

class InvalidS3UsEast1RegionalEndpointConfigError(BotoCoreError):
    fmt: str

class InvalidSTSRegionalEndpointsConfigError(BotoCoreError):
    fmt: str

class StubResponseError(BotoCoreError):
    fmt: str

class StubAssertionError(StubResponseError, AssertionError): ...
class UnStubbedResponseError(StubResponseError): ...

class InvalidConfigError(BotoCoreError):
    fmt: str

class InfiniteLoopConfigError(InvalidConfigError):
    fmt: str

class RefreshWithMFAUnsupportedError(BotoCoreError):
    fmt: str

class MD5UnavailableError(BotoCoreError):
    fmt: str

class MetadataRetrievalError(BotoCoreError):
    fmt: str

class UndefinedModelAttributeError(Exception): ...

class MissingServiceIdError(UndefinedModelAttributeError):
    fmt: str
    kwargs: Any = ...
    def __init__(self, **kwargs: Any) -> None: ...

class SSOError(BotoCoreError):
    fmt: str

class SSOTokenLoadError(SSOError):
    fmt: str

class UnauthorizedSSOTokenError(SSOError):
    fmt: str

class CapacityNotAvailableError(BotoCoreError):
    fmt: str

class InvalidProxiesConfigError(BotoCoreError):
    fmt: str
