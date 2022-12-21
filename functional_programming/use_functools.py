from functools import total_ordering, reduce
from typing import NamedTuple, Any


@total_ordering
class Card(NamedTuple):
    rank: int
    suit: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank == other.rank
        elif isinstance(other, int):
            return self.rank == other
        return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.rank < other.rank
        elif isinstance(other, int):
            return self.rank < other
        return NotImplemented


if __name__ == "__main__":
    c2s = Card(2, "\u2660")
    c2h = Card(2, "\u2665")
    c3h = Card(3, "\u2665")
    c4c = Card(4, "\u2663")
    print(c2h == c2s)
    print(c2h == 2)
    print(2 == c2h)

    print(c2s <= c3h < c4c)
    print(c3h >= c3h)
    print(c3h > c2s)
    print(c4c != c2s)

    r = reduce(lambda x, y: x + y**2, [2, 4, 4, 4, 5, 5, 7, 9])
    print(r)
