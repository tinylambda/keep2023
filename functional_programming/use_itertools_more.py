import math
from itertools import product
from typing import Iterator, Tuple, NamedTuple

from PIL import Image

Point = Tuple[int, int]
RGB = Tuple[int, int, int]
Pixel = Tuple[Point, RGB]


class Color(NamedTuple):
    rgb: Tuple[int, int, int]
    name: str


def pixel_iter(img: Image) -> Iterator[Pixel]:
    w, h = img.size
    return ((c, img.getpixel(c)) for c in product(range(w), range(h)))


def euclidean(pixel: Pixel, color: Color):
    return math.sqrt(sum(map(lambda x, y: (x - y) ** 2, pixel, color.rgb)))


def manhattan(pixel: RGB, color: Color):
    return sum(map(lambda x, y: abs(x - y), pixel, color.rgb))


if __name__ == "__main__":
    with Image.open("data/example.jpeg") as img:
        print(list(pixel_iter(img)))
