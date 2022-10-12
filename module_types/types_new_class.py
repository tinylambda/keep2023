import types

from base import keep_logger


class Matter:
    pass


cls_live_beings = types.new_class(
    "LivingBeings",
    (Matter,),
    {"metaclass": type},
    lambda ns: None,
)
cls_live_beings.__module__ = __name__


class Human(cls_live_beings):
    pass


class Teacher(Human):
    pass


class Student(Human):
    pass


if __name__ == "__main__":
    # the generated class is just a normal class
    keep_logger.info("%s", cls_live_beings)
    keep_logger.info("%s", Human)
    keep_logger.info("%s", Teacher)
    keep_logger.info("%s", issubclass(Student, cls_live_beings))  # True
    keep_logger.info("%s", issubclass(Student, Human))  # True
    keep_logger.info("%s", issubclass(Student, Teacher))  # False
