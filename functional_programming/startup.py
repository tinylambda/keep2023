from base import keep_logger


def sumr(seq):
    """sum in recursive way"""
    if len(seq) == 0:
        return 0
    return seq[0] + sumr(seq[1:])


def until(n, filter_func, v):
    if v == n:
        return []
    if filter_func(v):
        return [v] + until(n, filter_func, v + 1)
    else:
        return until(n, filter_func, v + 1)


def next_(n, x):
    return (x + n / x) / 2


def repeat(f, a):
    yield a
    for v in repeat(f, f(a)):
        yield v


def within(e, iterable):
    def head_tail(e, a, iterable):
        b = next(iterable)
        if abs(a - b) <= e:
            return b
        return head_tail(e, b, iterable)

    return head_tail(e, next(iterable), iterable)


def sqrt(a0, e, n):
    return within(e, repeat(lambda x: next_(n, x), a0))


if __name__ == "__main__":
    l = [1, 2, 3, 4, 5]
    keep_logger.info("sum using recursion: %s", sumr(l))

    mult_3_5 = lambda x: x % 3 == 0 or x % 5 == 0
    l = until(10, mult_3_5, 0)
    keep_logger.info("use until to gen list: %s", l)

    keep_logger.info(
        "gen exp: %s", sum(n for n in range(1, 10) if n % 3 == 0 or n % 5 == 0)
    )

    n = 2
    f = lambda x: next_(n, x)
    a0 = 1.0
    est_list = [round(x, 4) for x in (a0, f(a0), f(f(a0)), f(f(f(a0))))]
    keep_logger.info("est list: %s", est_list)

    keep_logger.info("sqrt: %s", sqrt(1.0, 0.0001, 2))
