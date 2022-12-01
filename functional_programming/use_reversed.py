from typing import Iterator

from base import keep_logger


def digits(x: int, b: int) -> Iterator[int]:
    if x == 0:
        return
    yield x % b
    for d in digits(x // b, b):
        yield d


def to_base(x: int, b: int) -> Iterator[int]:
    return reversed(tuple(digits(x, b)))


if __name__ == "__main__":
    num_base10 = 1024
    keep_logger.info("%s", list(digits(num_base10, 2)))
    keep_logger.info("%s", list(to_base(num_base10, 2)))
