from typing import Any

from botocore.compat import OrderedDict as OrderedDict
from botocore.endpoint import DEFAULT_TIMEOUT as DEFAULT_TIMEOUT
from botocore.endpoint import MAX_POOL_CONNECTIONS as MAX_POOL_CONNECTIONS
from botocore.exceptions import (
    InvalidMaxRetryAttemptsError as InvalidMaxRetryAttemptsError,
)
from botocore.exceptions import (
    InvalidRetryConfigurationError as InvalidRetryConfigurationError,
)
from botocore.exceptions import InvalidRetryModeError as InvalidRetryModeError
from botocore.exceptions import (
    InvalidS3AddressingStyleError as InvalidS3AddressingStyleError,
)

class Config:
    OPTION_DEFAULTS: OrderedDict[str, None]
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def merge(self, other_config: Any) -> Any: ...
