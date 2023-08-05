from typing import Any, Callable, Generator, Optional, Union

YieldType = Optional[Union[float, int]]
GeneratorType = Generator[YieldType, None, None]
DoneCallbackType = Union[Callable[..., Any]]
CancelFuncType = Union[Callable[..., None]]

__all__ = [
    "YieldType",
    "GeneratorType",
    "DoneCallbackType",
    "CancelFuncType",
]
