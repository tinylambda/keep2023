import math
from functools import wraps
from typing import Callable, Any, TypeVar, Optional, cast

FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def nullable(function: F) -> F:
    @wraps(function)
    def null_wrapper(arg: Optional[Any]) -> Optional[Any]:
        return None if arg is None else function(arg)

    return cast(F, null_wrapper)


@nullable
def nlog(x: Optional[float]) -> Optional[float]:
    return math.log(x)


@nullable
def nround4(x: Optional[float]) -> Optional[float]:
    return round(x, 4)


if __name__ == "__main__":
    some_data = [10, 100, None, 50, 60]
    scaled = map(nlog, some_data)
    print(list(scaled))
