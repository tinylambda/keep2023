import csv
import pprint
from collections import defaultdict
from typing import (
    Text,
    List,
    Iterable,
    TextIO,
    Optional,
    Iterator,
    Callable,
    TypeVar,
    Tuple,
    cast,
    NamedTuple,
    Dict,
)

T_ = TypeVar("T_")
D_ = TypeVar("D_")
K_ = TypeVar("K_")
RawPairIter = Iterable[Tuple[float, float]]


class Pair(NamedTuple):
    x: float
    y: float


RankedPair = Tuple[int, Pair]
Rank2Pair = Tuple[int, RankedPair]


pairs: Callable[[RawPairIter], List[Pair]] = lambda source: list(
    Pair(*row) for row in source
)


def series(n: int, row_iter: Iterable[List[T_]]) -> Iterator[Pair]:
    for row in row_iter:
        yield cast(Pair, tuple(row[n * 2 : n * 2 + 2]))


def row_iter(source: TextIO) -> Iterable[List[Text]]:
    rdr = csv.reader(source, delimiter="\t")
    return rdr


def float_none(data: Optional[Text]) -> Optional[float]:
    try:
        data_f = float(data)
        return data_f
    except ValueError:
        return None


def head_map_filter(row_iter: Iterator[List[Optional[Text]]]) -> Iterator[List[float]]:
    R_Text = List[Optional[Text]]
    R_Float = List[Optional[float]]

    float_row: Callable[[R_Text], R_Float] = lambda row: list(map(float_none, row))
    all_numeric: Callable[[R_Float], bool] = lambda row: all(row) and len(row) == 8

    return filter(all_numeric, map(float_row, row_iter))


def rank_y(pairs: Iterable[Pair]) -> Iterator[RankedPair]:
    return enumerate(sorted(pairs, key=lambda p: p.y))


def rank_x(ranked_pairs: Iterable[RankedPair]) -> Iterator[Rank2Pair]:
    return enumerate(sorted(ranked_pairs, key=lambda rank: rank[1].x))


x_rank = lambda ranked: ranked[0]
y_rank = lambda ranked: ranked[1][0]
raw = lambda ranked: ranked[1][1]


def rank(
    data: Iterable[D_], key: Callable[[D_], K_] = lambda obj: cast(K_, obj)
) -> Iterator[Tuple[float, D_]]:
    def build_duplicates(
        duplicates: Dict[K_, List[D_]], data_iter: Iterator[D_], key: Callable[[D_], K_]
    ) -> Dict[K_, List[D_]]:
        for item in data_iter:
            duplicates[key(item)].append(item)
        return duplicates

    def rank_out(
        duplicates: Dict[K_, List[D_]], key_iter: Iterator[K_], base: int = 0
    ) -> Iterator[Tuple[float, D_]]:
        for k in key_iter:
            dups = len(duplicates[k])
            for value in duplicates[k]:
                yield (base + 1 + base + dups) / 2, value

            base += dups

    duplicates = build_duplicates(defaultdict(list), iter(data), key)
    return rank_out(duplicates, iter(sorted(duplicates)), 0)


if __name__ == "__main__":
    with open("data/Anscombe.txt") as source:
        data = list(head_map_filter(row_iter(source)))
        series_1 = pairs(series(0, data))
        series_2 = pairs(series(1, data))
        series_3 = pairs(series(2, data))
        series_4 = pairs(series(3, data))

        y_rank = list(rank_y(series_1))
        xy_rank = list(rank_y(series_1))
        pprint.pprint(xy_rank)

        sample_data = [0.8, 1.2, 1.2, 1.2, 1.2, 2.3, 18]
        pprint.pprint(list(rank(sample_data)))
