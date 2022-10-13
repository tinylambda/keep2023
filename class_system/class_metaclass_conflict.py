class Meta(type):
    pass


class MetaA(Meta):
    pass


class MetaX(type):
    pass


class A(metaclass=MetaA):
    pass


class B(metaclass=MetaX):
    pass


# A and B have different metaclass that with no inheritance relationship,
# so it will confuse about how to construct the class
class C(A, B):
    pass
