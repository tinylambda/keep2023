import operator
from functools import reduce
from typing import Iterable


def prod(data: Iterable[int]) -> int:
    # return reduce(lambda x, y: x * y, data, initial=1)
    return reduce(operator.mul, data, 1)


def fact(n: int) -> int:
    f = {
        n == 0: lambda n: 1,
        n == 1: lambda n: 1,
        n == 2: lambda n: 2,
        n > 2: lambda n: fact(n - 1) * n,
    }[True]
    return f(n)


def non_strict_max(a, b):
    f = {
        a >= b: lambda: a,
        a <= b: lambda: b,
    }[True]
    return f()


if __name__ == "__main__":
    r = prod(iter([1, 2, 3]))
    print(r)

    print(fact(11))
    print(non_strict_max(100, 101))
    print(non_strict_max(100, 100))
