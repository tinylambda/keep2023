from base import keep_logger


class A:
    DOMAIN = "PAYMENT"

    def __new__(cls, *args, **kwargs):
        real_obj = super().__new__(cls)
        keep_logger.info("A cls: %s, args: %s, kwargs: %s", cls, args, kwargs)
        keep_logger.info("A constructing object: %s", real_obj)
        keep_logger.info("A has x ? %s", hasattr(real_obj, "x"))
        keep_logger.info("A has DOMAIN ? %s", hasattr(real_obj, "DOMAIN"))
        return real_obj

    def __init__(self, x):
        keep_logger.info("A initializing object: %s", self)
        self.x = x


class Meta(type):
    def __new__(mcs, *args, **kwargs):
        real_cls = super().__new__(mcs, *args, **kwargs)
        keep_logger.info("Meta mcs: %s, args: %s, kwargs: %s", mcs, args, kwargs)
        keep_logger.info("Meta has DOMAIN ? %s", hasattr(real_cls, "DOMAIN"))
        return real_cls

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(cls, "DOMAIN"):
            keep_logger.info("%s belongs to domain: %s", cls, getattr(cls, "DOMAIN"))
        else:
            keep_logger.info("%s belongs to no domain", cls)


class B(metaclass=Meta):
    pass


class C(metaclass=Meta):
    DOMAIN = "PAYMENT"


if __name__ == "__main__":
    A(x=100)
