# tail call optimization
import math

from base import keep_logger


def isprimer(n: int) -> bool:
    def isprime(k: int, coprime: int) -> bool:
        if k < coprime * coprime:
            return True
        if k % coprime == 0:
            return False
        return isprime(k, coprime + 2)

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return isprime(n, 3)


def isprimei(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(1 + math.sqrt(n)), 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    num = 7919**2
    keep_logger.info("isprimei(%s): %s", num, isprimei(num))
    # raise RecursionError
    keep_logger.info("isprimer(%s): %s", num, isprimer(num))
