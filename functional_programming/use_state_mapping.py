import bisect
from abc import ABC
from collections import namedtuple
from collections.abc import Mapping
from typing import Iterable, Tuple, Any

from base import keep_logger

Color = namedtuple("Color", ("red", "green", "blue", "name"))


class StaticMapping(Mapping, ABC):
    def __init__(self, iterable: Iterable[Tuple[Any, Any]]) -> None:
        self._data = tuple(iterable)
        self._keys = tuple(sorted(key for key, _ in self._data))

    def __getitem__(self, item):
        ix = bisect.bisect_left(self._keys, item)
        if ix != len(self._keys) and self._keys[ix] == item:
            return self._data[ix][1]
        raise ValueError("{0!r} not found".format(item))

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)


if __name__ == "__main__":
    sequence = (
        Color(red=239, green=222, blue=205, name="Almond"),
        Color(red=205, green=149, blue=117, name="Antique Brass"),
    )

    name_map = dict((c.name, c) for c in sequence)
    keep_logger.info("name_map: %s", name_map)

    name_map_2 = StaticMapping((c.name, c) for c in sequence)
    keep_logger.info("name_map_2['Almond']: %s", name_map_2["Almond"])
    keep_logger.info("name_map_2['Antique Brass']: %s", name_map_2["Antique Brass"])
