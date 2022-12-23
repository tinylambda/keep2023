import operator
from functools import reduce
from typing import Iterable


def prod(data: Iterable[int]) -> int:
    # return reduce(lambda x, y: x * y, data, initial=1)
    return reduce(operator.mul, data, 1)


if __name__ == "__main__":
    r = prod(iter([1, 2, 3]))
    print(r)
