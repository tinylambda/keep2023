import decimal
import math
from functools import wraps
from typing import Callable, Any, TypeVar, Optional, cast, Tuple

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


def bad_data(function: F) -> F:
    @wraps(function)
    def wrap_bad_data(text: str, *args: Any, **kwargs: Any) -> Any:
        try:
            return function(text, *args, **kwargs)
        except (ValueError, decimal.InvalidOperation):
            cleaned = text.replace(",", "")
            return function(cleaned, *args, **kwargs)

    return cast(F, wrap_bad_data)


bd_int = bad_data(int)
bd_float = bad_data(float)
bd_decimal = bad_data(decimal.Decimal)


def clean_list(text: str, char_list: Tuple[str, ...]) -> str:
    if char_list:
        return clean_list(text.replace(char_list[0], ""), char_list[1:])
    return text


def bad_char_remove(*char_list: str) -> Callable[[F], F]:
    def cr_decorator(function: F) -> F:
        @wraps(function)
        def wrap_char_remove(text: str, *args, **kw):
            try:
                return function(text, *args, **kw)
            except (ValueError, decimal.InvalidOperation):
                cleaned = clean_list(text, char_list)
                return function(cleaned, *args, **kw)

        return cast(F, wrap_char_remove)

    return cr_decorator


@bad_char_remove("$", ",")
def currency(text: str, **kw) -> decimal.Decimal:
    return decimal.Decimal(text, **kw)


if __name__ == "__main__":
    some_data = [10, 100, None, 50, 60]
    scaled = map(nlog, some_data)
    print(list(scaled))

    print(bd_int("13"))
    print(bd_int("13,12"))

    print(currency("13"))
    print(currency("13,12"))
    print(currency("$13,12"))
