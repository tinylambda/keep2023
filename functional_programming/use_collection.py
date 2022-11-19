import xml.etree.ElementTree
from pathlib import Path
from typing import TextIO, Text, List, Iterable, Tuple, Any, Iterator, TypeVar

from base import keep_logger

fst = lambda x: x[0]
snd = lambda x: x[1]

Rows = Iterable[List[Text]]
LL_Text = Tuple[Text, Text]
Item_Iter = Iterator[Any]

T_ = TypeVar("T_")
Pairs_Iter = Iterator[Tuple[T_, T_]]


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


if __name__ == "__main__":
    geo_xml = Path(__file__).parent / "data" / "geo.xml"
    with open(geo_xml, "r") as geo_file_obj:
        v1 = tuple(lat_lon_kml(row_iter_kml(geo_file_obj)))
        keep_logger.info("%s", v1)

    points = [1.0, 2.0, 2.1, 2.3, 1.2, 2.3, 3.0]
    for item in legs(iter(points)):
        keep_logger.info("%s", item)
