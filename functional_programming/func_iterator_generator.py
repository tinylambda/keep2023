from decimal import Decimal
from typing import Callable, Text, Optional

from base import keep_logger


def m(n: int) -> int:
    """A pure function example"""
    return 2**n - 1


# strategy pattern
class Mersennel:
    def __init__(self, algorithm: Callable[[int], int]) -> None:
        self.pow2 = algorithm

    def __call__(self, arg: int) -> int:
        return self.pow2(arg)


def shifty(b: int) -> int:
    return 1 << b


def multy(b: int) -> int:
    if b == 0:
        return 1
    return 2 * multy(b - 1)


def faster(b: int) -> int:
    if b == 0:
        return 1
    if b % 2 == 1:
        return 2 * faster(b - 1)
    t = faster(b // 2)
    return t * t


# strategy pattern end

# use string
def clean_decimal(text: Text) -> Optional[Decimal]:
    if text is None:
        return None
    return Decimal(text.replace("$", "").replace(",", ""))


def replace(str: Text, a: Text, b: Text) -> Text:
    return str.replace(a, b)


def remove(str: Text, chars: Text) -> Text:
    if chars:
        return remove(str.replace(chars[0], ""), chars[1:])
    return str


def clean_decimal_v2(text: Text) -> Optional[Decimal]:
    if text is None:
        return None
    return Decimal(remove(text, "$,"))


# use string end

# use tuple


if __name__ == "__main__":
    m1 = Mersennel(shifty)
    m2 = Mersennel(multy)
    m3 = Mersennel(faster)

    num = 10
    keep_logger.info("m1: %s", m1(num))
    keep_logger.info("m2: %s", m2(num))
    keep_logger.info("m3: %s", m3(num))

    num_txt = "$100,100"
    keep_logger.info("clean_decimal: %s", clean_decimal(num_txt))
    keep_logger.info("clean_decimal_v2: %s", clean_decimal_v2(num_txt))
