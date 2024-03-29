# type: ignore


import xml.etree.ElementTree
from collections import Counter, defaultdict
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Sequence,
    Text,
    TextIO,
    Tuple,
    TypeVar,
    NamedTuple,
    cast,
)

from base import keep_logger

fst = lambda x: x[0]
snd = lambda x: x[1]

Rows = Iterable[List[Text]]
LL_Text = Tuple[Text, Text]
Item_Iter = Iterator[Any]

Text_Iter = Iterable[Tuple[Text, Text]]
LL_Iter = Iterable[Tuple[float, float]]

T_ = TypeVar("T_")
Pairs_Iter = Iterator[Tuple[T_, T_]]

Point = Tuple[float, float]
Leg_Raw = Tuple[Point, Point]
Point_Func = Callable[[Point, Point], float]
Leg_D = Tuple[Point, Point, float]
Leg_P_D = Tuple[Leg_Raw, ...]

Conv_F = Callable[[float], float]
# Leg = Tuple[Any, Any, float]


class Point(NamedTuple):
    latitude: float
    longitude: float


class Leg(NamedTuple):
    start: Point
    end: Point
    distance: float


S_ = TypeVar("S_")
K_ = TypeVar("K_")

MI = 3959
NM = 3440
KM = 6371


def cons_distance(
    distance: Point_Func, legs_iter: Iterable[Leg_Raw]
) -> Iterator[Leg_D]:
    return ((start, end, round(distance(start, end), 4)) for start, end in legs_iter)


def cons_distance3(
    distance: Point_Func, legs_iter: Iterable[Leg_Raw]
) -> Iterator[Leg_P_D]:
    return (leg + (round(distance(*leg), 4),) for leg in legs_iter)


def comma_split(text: Text) -> List[Text]:
    return text.split(",")


def row_iter_kml(file_obj: TextIO) -> Iterable[List[Text]]:
    ns_map = {
        "ns0": "http://www.opengis.net/kml/2.2",
        "ns1": "http://www.google.com/kml/ext/2.2",
    }
    path_to_points = "./ns0:Document/ns0:Folder/ns0:Placemark/ns0:Point/ns0:coordinates"
    doc = xml.etree.ElementTree.parse(file_obj)
    return (
        comma_split(Text(coordinates.text))
        for coordinates in doc.findall(path_to_points, ns_map)
    )


def pick_lat_lon(lon: Text, lat: Text, alt: Text) -> Tuple[Text, Text]:
    return lat, lon


def lat_lon_kml(row_iter: Rows) -> Iterable[LL_Text]:
    return (pick_lat_lon(*row) for row in row_iter)


def pairs(iterator: Item_Iter) -> Pairs_Iter:
    def pair_from(head: Any, iterable_tail: Item_Iter) -> Pairs_Iter:
        nxt = next(iterable_tail)
        yield head, nxt
        yield from pair_from(nxt, iterable_tail)

    try:
        return pair_from(next(iterator), iterator)
    except StopIteration:
        return iter([])


def legs(lat_lon_iter: Iterator[T_]) -> Pairs_Iter:
    begin = next(lat_lon_iter)
    for end in lat_lon_iter:
        yield begin, end
        begin = end


def float_from_pair(lat_lon_iter: Text_Iter) -> LL_Iter:
    return ((float(lat), float(lon)) for lat, lon in lat_lon_iter)


def float_lat_lon(row_iter: Iterator[Tuple[str, ...]]) -> Iterator[Tuple[float, ...]]:
    return (tuple(map(float, pick_lat_lon(*row))) for row in row_iter)


def haversine(p1: Point, p2: Point, R: float = NM) -> float:
    lat_1, lon_1 = p1
    lat_2, lon_2 = p2
    delta_lat = radians(lat_2 - lat_1)
    delta_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sqrt(
        sin(delta_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(delta_lon / 2) ** 2
    )
    c = 2 * asin(a)
    return R * c


def f_start(s, e, d):
    return s


def f_end(s, e, d):
    return e


def f_dist(s, e, d):
    return d


def f_latitude(lat, lon):
    return lat


def f_longitude(lat, lon):
    return lon


def to_miles(x):
    return x * 5280 / 6076.12


def to_km(x):
    return x * 1.852


def to_nm(x):
    return x


def convert(conversion: Conv_F, _trip: Iterable[Leg]) -> Iterator[float]:
    return (conversion(distance) for start, end, distance in _trip)


def group_sort1(trip: Iterable[Leg]) -> Dict[int, int]:
    def group(data: Iterable[T_]) -> Iterable[Tuple[T_, int]]:
        previous, count = None, 0
        for d in sorted(data):
            if d == previous:
                count += 1
            elif previous is not None:
                yield previous, count
                previous, count = d, 1
            elif previous is None:
                previous, count = d, 1
            else:
                raise Exception("Bad bad design problem")
        yield previous, count

    quantized = (int(5 * (dist // 5)) for beg, end, dist in trip)
    return dict(group(quantized))


def group_by(key: Callable[[S_], K_], data: Sequence[S_]) -> Dict[K_, List[S_]]:
    def group_into(
        key: Callable[[S_], K_],
        collection: Sequence[S_],
        dictionary: Dict[K_, List[S_]],
    ):
        if len(collection) == 0:
            return dictionary
        head, *tail = collection
        dictionary[key(head)].append(head)
        return group_into(key, tail, dictionary)

    return group_into(key, data, defaultdict(list))


def partition(key: Callable[[S_], K_], data: Iterable[S_]) -> Dict[K_, List[S_]]:
    dictionary: Dict[K_, List[S_]] = defaultdict(list)
    for head in data:
        dictionary[key(head)].append(head)
    return dictionary


def binned_distance(leg):
    return 5 * (leg[2] // 5)


def sum_f(function: Callable[[Any], float], data: Iterable) -> float:
    return sum(function(x) for x in data)


def get_trip(file_path: str) -> List[Leg]:
    with open(file_path, "r") as source:
        path_iter = float_lat_lon(row_iter_kml(cast(TextIO, source)))
        pair_iter = legs(path_iter)
        trip_iter = (
            Leg(start, end, round(haversine(start, end), 4)) for start, end in pair_iter
        )
        trip = list(trip_iter)
        return trip


if __name__ == "__main__":
    geo_xml = Path(__file__).parent / "data" / "geo.xml"
    with open(geo_xml, "r") as geo_file_obj:
        trip = (
            (start, end, round(haversine(start, end), 4))
            for start, end in legs(
                float_from_pair(lat_lon_kml(row_iter_kml(geo_file_obj)))
            )
        )
        trip_tuple = tuple(trip)
        for start, end, dist in trip_tuple:
            keep_logger.info("%s, %s, %s", start, end, dist)

        # points = [1.0, 2.0, 2.1, 2.3, 1.2, 2.3, 3.0]
        # for item in legs(iter(points)):
        #     keep_logger.info("%s", item)

        def by_dist(leg: Tuple[Any, Any, Any]) -> Any:
            lat, lon, _dist = leg
            return _dist

        long = max(trip_tuple, key=by_dist)
        short = min(trip_tuple, key=by_dist)
        keep_logger.info("long: %s, short: %s", long, short)

        keep_logger.info(
            "trip_m: %s", list(map(to_miles, (f_dist(*item) for item in trip_tuple)))
        )

        trip_long = list(filter(lambda leg: f_dist(*leg) >= 50, trip_tuple))
        keep_logger.info("trip_long: %s", trip_long)

        keep_logger.info("convert: %s", list(convert(to_miles, trip_tuple)))

    with open(geo_xml, "r") as geo_file_obj:
        path = float_from_pair(lat_lon_kml(row_iter_kml(geo_file_obj)))
        trip2 = tuple(cons_distance(haversine, legs(path)))
        keep_logger.info("trip2: %s", trip2)

    with open(geo_xml, "r") as geo_file_obj:
        path = float_from_pair(lat_lon_kml(row_iter_kml(geo_file_obj)))
        trip3 = tuple(cons_distance3(haversine, legs(path)))
        keep_logger.info("trip3: %s", trip3)

    # quantized
    quantized = (5 * (dist // 5) for start, stop, dist in trip_tuple)
    quantized_counter = Counter(quantized)
    keep_logger.info("use counter: %s", quantized_counter.most_common())

    keep_logger.info("use group_sort1: %s", group_sort1(trip_tuple))

    by_distance = group_by(binned_distance, trip_tuple)
    keep_logger.info("group_by <----")
    for distance in sorted(by_distance):
        keep_logger.info("%s: %s", distance, by_distance[distance])
    keep_logger.info("group_by ---->")

    by_distance = partition(binned_distance, trip_tuple)

    keep_logger.info("partition <----")
    for distance in sorted(by_distance):
        keep_logger.info("%s: %s", distance, by_distance[distance])
    keep_logger.info("partition ---->")

    keep_logger.info("north most <----")
    for distance in sorted(by_distance):
        keep_logger.info(
            "%s: %s",
            distance,
            max(by_distance[distance], key=lambda pt: f_latitude(*(f_start(*pt)))),
        )
    keep_logger.info("north most ---->")

    first_leg = Leg(
        Point(29.050501, -80.651169), Point(27.186001, -80.139503), 115.1751
    )
    keep_logger.info("use namedtuple: %s", first_leg.start.latitude)

    keep_logger.info("%s", get_trip(geo_xml))
