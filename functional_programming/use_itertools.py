import csv
import glob
import operator
import pprint
import random
from contextlib import ExitStack
from itertools import count, repeat, cycle, accumulate, chain, groupby
from typing import TypeVar, Callable, Iterator, Tuple, cast, TextIO, List

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


def randseq(limit):
    while True:
        yield random.randrange(limit)


def readfiles(*filenames: str) -> Iterator[List[str]]:
    with ExitStack() as stack:
        files = [
            stack.enter_context(cast(TextIO, open(name, "r"))) for name in filenames
        ]
        readers = map(lambda f: csv.reader(f, delimiter=","), files)
        yield from chain(*readers)


randomized = randseq(100)
all = repeat(0)
subset = cycle(range(100))
choose = lambda rule: (x == 0 for x in rule)


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

    data = range(20)
    pprint.pprint([v for v, pick in zip(data, choose(all)) if pick])
    pprint.pprint([v for v, pick in zip(data, choose(subset)) if pick])
    pprint.pprint([v for v, pick in zip(data, choose(randomized)) if pick])

    data = [1, 4, 5, 6, 4, 3, 5, 6, 7, 239, 12]
    pprint.pprint(data)

    m = accumulate(data, max)
    pprint.pprint(list(m))

    r = accumulate(data, operator.add, initial=10000)
    pprint.pprint(list(r))

    filenames: List[str] = glob.glob("data/files/*.csv")
    for item in readfiles(*filenames):
        pprint.pprint(item)

    data = [
        {"g": "1", "name": "felix"},
        {"g": "1", "name": "fanny"},
        {"g": "2", "name": "tom"},
        {"g": "2", "name": "jerry"},
    ]
    group_iter = groupby(data, key=lambda x: x["g"])
    for k, items in group_iter:
        print(k, ": ", list(items))
