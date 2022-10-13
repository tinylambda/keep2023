from base import keep_logger


class Field:
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        keep_logger.info("__set_name__(%s, %s, %s)", self, owner, name)
        self.name = name
        self.internal_name = f"__{self.name}"

    def __get__(self, instance, owner):
        keep_logger.info("__get__(%s, %s, %s)", self, instance, owner)
        if instance is None:
            return self
        return getattr(instance, self.internal_name)

    def __set__(self, instance, value):
        keep_logger.info("__set__(%s, %s, %s)", self, instance, value)
        setattr(instance, self.internal_name, value)


class Model:
    name: str = Field()
    birthday = Field()


if __name__ == "__main__":
    model = Model()
    model.name = "Felix"
    model.birthday = "1987"
    keep_logger.info("%s", model.__dict__)
