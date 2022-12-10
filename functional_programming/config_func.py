import math
from typing import Any, Callable, Optional, Iterable

from base import keep_logger


class NullAware:
    def __init__(self, some_func: Callable[[Any], Any]) -> None:
        self.some_func = some_func

    def __call__(self, arg: Optional[Any]) -> Optional[Any]:
        return None if arg is None else self.some_func(arg)


class SumFilter:
    __slots__ = ["filter", "function"]

    def __init__(
        self, filter: Callable[[Any], bool], func: Callable[[Any], float]
    ) -> None:
        self.filter = filter
        self.function = func

    def __call__(self, iterable: Iterable) -> float:
        return sum(self.function(x) for x in iterable if self.filter(x))


if __name__ == "__main__":
    some_data = [10, 100, None, 50, 60]
    null_log_scale = NullAware(math.log)
    scaled = map(null_log_scale, some_data)
    keep_logger.info("scaled: %s", list(scaled))

    count_not_none = SumFilter(lambda x: x is not None, lambda x: 1)
    keep_logger.info("count_not_none: %s", count_not_none(some_data))
