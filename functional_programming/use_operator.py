import operator
from functools import reduce
from typing import Iterable, Sequence

from pymonad.tools import curry


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


@curry(4)
def systolic_bp(bmi, age, gender_male, treatment):
    return 68.15 + 0.58 * bmi + 0.65 * age + 0.94 * gender_male + 6.44 * treatment


@curry(2)
def myreduce(function, iterable_or_sequence):
    if isinstance(iterable_or_sequence, Sequence):
        iterator = iter(iterable_or_sequence)
    else:
        iterator = iterable_or_sequence
    s = next(iterator)
    for v in iterator:
        s = function(s, v)
    return s


if __name__ == "__main__":
    r = prod(iter([1, 2, 3]))
    print(r)

    print(fact(11))
    print(non_strict_max(100, 101))
    print(non_strict_max(100, 100))

    print(systolic_bp()(25, 50, 1, 0))
    print(systolic_bp()(25, 50, 0, 1))

    treated = systolic_bp(25, 50, 0)
    print(treated)
    print(treated(0))
    print(treated(1))

    g_t = systolic_bp(25, 50)
    print(g_t)
    print(g_t(1, 0))
    print(g_t(0, 1))

    sum = myreduce(operator.add)
    print(sum([1, 2, 3]))

    max = myreduce(lambda x, y: x if x > y else y)
    print(max([1, 2, 3]))
