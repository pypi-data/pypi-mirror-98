import logging
from typing import Any, Dict, Tuple

class NullHandler(logging.Handler):
    def emit(self, record: Any) -> None: ...

log: logging.Logger
ScalarTypes: Tuple[str, ...]
BOTOCORE_ROOT: str

class UNSIGNED:
    def __copy__(self) -> UNSIGNED: ...
    def __deepcopy__(self, memodict: object) -> UNSIGNED: ...

def xform_name(
    name: str, sep: str = ..., _xform_cache: Dict[Tuple[str, str], str] = ...
) -> str: ...
