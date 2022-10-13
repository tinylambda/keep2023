from base import keep_logger


class A:
    x = 100

    def __init__(self, x=-100):
        self.x = x


if __name__ == "__main__":
    a = A()
    keep_logger.info("%s", a.x)  # should be -100
    keep_logger.info("%s", a.__class__.x)  # should be 100
