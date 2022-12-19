import csv
import glob
import operator
import pprint
import random
from contextlib import ExitStack
from itertools import (
    count,
    repeat,
    cycle,
    accumulate,
    chain,
    groupby,
    compress,
    islice,
    dropwhile,
    filterfalse,
    starmap,
    tee,
)
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


def mean(iterator: Iterator[float]) -> float:
    it0, it1 = tee(iterator, 2)
    N = sum(1 for x in it0)
    s1 = sum(x for x in it1)
    return s1 / N


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
    pprint.pprint("Choose:")
    pprint.pprint([v for v, pick in zip(data, choose(all)) if pick])
    pprint.pprint([v for v, pick in zip(data, choose(subset)) if pick])
    pprint.pprint([v for v, pick in zip(data, choose(randomized)) if pick])

    pprint.pprint("Choose use compress:")
    pprint.pprint(list(compress(data, choose(all))))
    subset = cycle(range(100))
    pprint.pprint(list(compress(data, choose(subset))))
    pprint.pprint(list(compress(data, choose(randomized))))

    pprint.pprint("Accumulate:")
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

    pprint.pprint("islice: ")
    data = [1, 4, 5, 6, 4, 3, 5, 6, 7, 239, 12]
    pprint.pprint("data: %s" % data)
    pprint.pprint(list(zip(data[0::2], data[1::2])))

    pprint.pprint("islice islice:")
    flat_iter1 = iter(data)
    flat_iter2 = iter(data)
    pprint.pprint(
        list(zip(islice(flat_iter1, 0, None, 2), islice(flat_iter2, 1, None, 2)))
    )

    pprint.pprint("colors: ")
    with open("data/crayola.gpl", "rt") as source:
        rdr = csv.reader(cast(TextIO, source), delimiter="\t")
        rows = dropwhile(lambda row: row[0] != "#", rdr)
        # now rows contains the # row
        color_rows = islice(rows, 1, None)
        pprint.pprint(list(color_rows))

    pprint.pprint("filter/filterfalse:")
    data = [0, False, 1, 2]
    pprint.pprint("data: %s" % data)
    pprint.pprint("filter: %s" % list(filter(None, data)))
    pprint.pprint("filterfalse: %s" % list(filterfalse(None, data)))

    pprint.pprint("map/starmap: ")
    pprint.pprint(list(map(lambda x, y: x + y, (1, 2), (3, 4))))  # should be 4, 6
    pprint.pprint(list(starmap(lambda x, y: x + y, [(1, 2), (3, 4)])))  # should be 3, 7

    pprint.pprint("mean: %s" % mean(x for x in range(10)))
