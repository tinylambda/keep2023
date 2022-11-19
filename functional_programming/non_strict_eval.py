from base import keep_logger


def numbers():
    for i in range(1024):
        yield i


def sum_to(n: int) -> int:
    s: int = 0
    for i in numbers():
        if i == n:
            break
        s += i
    return s


if __name__ == "__main__":
    keep_logger.info("sum_to(10): %s", sum_to(10))
