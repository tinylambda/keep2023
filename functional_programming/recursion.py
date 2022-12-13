from typing import Callable, Any, Sequence, List, TypeVar, Iterable, Iterator

from base import keep_logger

D_ = TypeVar("D_")
R_ = TypeVar("R_")


def add(a: int, b: int) -> int:
    if a == 0:
        return b
    else:
        return add(a - 1, b + 1)


def fact(n: int) -> int:
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


def facti(n: int) -> int:
    if n == 0:
        return 1
    f = 1
    for i in range(2, n + 1):
        f = f * i
    return f


def fastexp(a: float, n: int) -> float:
    if n == 0:
        return 1
    elif n % 2 == 1:
        return a * fastexp(a, n - 1)
    else:
        t = fastexp(a, n // 2)
        return t * t


def fib(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


def fibi(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    f_n2, f_n1 = 1, 1
    for _ in range(3, n + 1):
        f_n2, f_n1 = f_n1, f_n2 + f_n1

    return f_n1


def mapr(f: Callable[[Any], Any], collection: Sequence[Any]) -> List[Any]:
    if len(collection) == 0:
        return []
    return mapr(f, collection[:-1]) + [f(collection[-1])]


def mapf(f: Callable[[D_], R_], C: Iterable[D_]) -> Iterator[R_]:
    return (f(x) for x in C)


def mapg(f: Callable[[D_], R_], C: Iterable[D_]) -> Iterator[R_]:
    for x in C:
        yield f(x)


def prodrc(collection: Sequence[float]) -> float:
    if len(collection) == 0:
        return 1
    return collection[0] * prodrc(collection[1:])


def prodri(items: Iterator[float]) -> float:
    try:
        head = next(items)
    except StopIteration:
        return 1
    return head * prodri(items)


def prodi(items: Iterable[float]) -> float:
    p = 1
    for n in items:
        p *= n
    return p


if __name__ == "__main__":
    keep_logger.info("%s", add(100, 20))
    # the following trigger RecursionError
    # keep_logger.info("%s", add(-100, 20))

    keep_logger.info("%s", fact(997))
    # the following trigger RecursionError
    # keep_logger.info("%s", fact(998))

    # this is ok
    keep_logger.info("%s", facti(998))
    keep_logger.info("facti(3): %s", facti(3))
    keep_logger.info("fact(3): %s", fact(3))

    keep_logger.info("fastexp(4, 3): %s", fastexp(4, 3))
    keep_logger.info("fastexp(4, 4): %s", fastexp(4, 4))

    keep_logger.info("fib(10): %s", fib(10))
    keep_logger.info("fibi(100): %s", fibi(100))

    keep_logger.info(
        "mapr(lambda x: x * 10, [1, 2, 3]): %s", mapr(lambda x: x * 10, [1, 2, 3])
    )

    keep_logger.info(
        "list(mapf(lambda x: x * 10, range(10))): %s",
        list(mapf(lambda x: x * 10, range(10))),
    )

    keep_logger.info(
        "list(mapg(lambda x: x * 10, range(10))): %s",
        list(mapg(lambda x: x * 10, range(10))),
    )

    keep_logger.info("prodrc([1, 2, 3, 4]): %s", prodrc([1, 2, 3, 4]))
    keep_logger.info("prodri(iter([1, 2, 3, 4])): %s", prodri(iter([1, 2, 3, 4])))
    keep_logger.info("prodi([1, 2, 3, 4]): %s", prodi([1, 2, 3, 4]))
