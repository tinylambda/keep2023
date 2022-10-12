import types

from base import keep_logger


class Meta(type):
    pass


class MetaA(Meta):
    pass


class MetaX(type):
    pass


class A(metaclass=Meta):
    pass


class B(A):
    pass


class C(metaclass=MetaA):
    pass


class D(metaclass=MetaX):
    pass


class E:
    pass


if __name__ == "__main__":
    bases = (E, C, B, A)
    meta, ns, kwds = types.prepare_class("X", bases, {"metaclass": type, "x": 100})
    keep_logger.info("%s, %s, %s", meta, ns, kwds)  # should be MetaA

    try:
        # simulate metaclass conflict
        bases = (E, C, B, A, D)
        meta, ns, kwds = types.prepare_class("X", bases, {"metaclass": type, "x": 100})
    except TypeError as e:
        keep_logger.error("Expected error", exc_info=e)
