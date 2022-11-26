from typing import TypeVar, Sequence, Tuple, List, Iterator

from base import keep_logger

ItemType = TypeVar("ItemType")
Flat = Sequence[ItemType]
Grouped = List[Tuple[ItemType, ...]]

Flat_Iter = Iterator[ItemType]
Grouped_Iter = Iterator[Tuple[ItemType, ...]]


def group_by_seq(n: int, sequence: Flat) -> Grouped:
    flat_iter = iter(sequence)
    full_sized_items = list(
        tuple(next(flat_iter) for i in range(n)) for row in range(len(sequence) // n)
    )
    trailer = tuple(flat_iter)
    if trailer:
        return full_sized_items + [trailer]
    else:
        return full_sized_items


def gen_tuple(n: int, iterable: Flat_Iter) -> Tuple[ItemType, ...]:
    r = []
    try:
        for i in range(n):
            item = next(iterable)
            r.append(item)
        return tuple(r)
    except StopIteration:
        return tuple(r)


def group_by_iter(n: int, iterable: Flat_Iter) -> Grouped_Iter:
    row = gen_tuple(n, iterable)
    while row:
        yield row
        row = gen_tuple(n, iterable)


with open("data/1000.txt") as raw_file:
    blocked_gen = (line.split() for line in raw_file)
    flatten_gen = (x for line in blocked_gen for x in line)
    flatten_list = list(flatten_gen)
    keep_logger.info("original: %s", flatten_list)

    flatten_iter = iter(flatten_list)
    grouped_gen = (
        tuple(next(flatten_iter) for i in range(5))
        for row in range(len(flatten_list) // 5)
    )
    keep_logger.info("use gen exp: %s", list(grouped_gen))

    group_list = group_by_seq(7, flatten_list)
    keep_logger.info("use group_by_seq: %s", group_list)

    group_iter = group_by_iter(7, iter(flatten_list))
    keep_logger.info("use group_by_iter: %s", list(group_iter))
