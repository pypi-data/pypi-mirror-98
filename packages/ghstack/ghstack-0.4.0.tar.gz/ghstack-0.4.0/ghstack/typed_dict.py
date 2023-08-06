from typing import Any, Dict

# TODO: do something better about this...
try:
    from mypy_extensions import TypedDict as TypedDict
except ImportError:
    # Avoid the dependency on the mypy_extensions package.
    # It is required, however, for type checking.
    def TypedDict(name, attrs, total=True):  # type: ignore
        return Dict[Any, Any]
