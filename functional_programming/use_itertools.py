import pprint
from itertools import count
from typing import TypeVar, Callable, Iterator, Tuple

_enumerate = lambda x, start=0: zip(count(start), x)


T_ = TypeVar("T_")
Generator = Iterator[Tuple[float, float]]
source: Generator = zip(count(0, 0.1), (0.1 * c for c in count()))
Extractor = Callable[[Tuple[float, float]], float]

x: Extractor = lambda x_y: x_y[0]
y: Extractor = lambda x_y: x_y[1]

Comparator = Callable[[Tuple[float, float]], bool]
neq: Comparator = lambda xy: abs(x(xy) - y(xy)) > 1.0e-12


def until(terminate: Callable[[T_], bool], iterator: Iterator[T_]) -> T_:
    i = next(iterator)
    if terminate(i):
        return i
    return until(terminate, iterator)


if __name__ == "__main__":
    sample_data = "word"
    pprint.pprint(list(_enumerate(iter(sample_data))))
    pprint.pprint(list(enumerate(iter(sample_data))))

    pprint.pprint(list(zip(count(1, 3), iter(sample_data))))  # this is better
    pprint.pprint(list((1 + 3 * e, x) for e, x in enumerate(iter(sample_data))))

    r = until(neq, source)
    pprint.pprint(r)

    source: Generator = zip(count(0, 0.1), (0.1 * c for c in count()))
    r = until(lambda xy: xy[0] != xy[1], source)
    pprint.pprint(r)
