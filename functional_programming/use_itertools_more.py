import math
import pprint
from collections import defaultdict
from itertools import product
from typing import Iterator, Tuple, NamedTuple

from PIL import Image

Point = Tuple[int, int]
RGB = Tuple[int, int, int]
Pixel = Tuple[Point, RGB]


class Color(NamedTuple):
    rgb: Tuple[int, int, int]
    name: str


colors = [
    Color(rgb=(239, 222, 205), name="Almond"),
    Color(rgb=(255, 255, 153), name="Canary"),
    Color(rgb=(28, 172, 120), name="Green"),
    Color(rgb=(48, 186, 143), name="Mountain Meadow"),
    Color(rgb=(255, 73, 108), name="Radical Red"),
    Color(rgb=(253, 94, 83), name="Sunset Orange"),
    Color(rgb=(255, 174, 66), name="Yellow Orange"),
]

xy: Point = lambda xyp_c: xyp_c[0][0]
p: RGB = lambda xyp_c: xyp_c[0][1]
c: Color = lambda xyp_c: xyp_c[1]


def pixel_iter(img: Image) -> Iterator[Pixel]:
    w, h = img.size
    return ((c, img.getpixel(c)) for c in product(range(w), range(h)))


def euclidean(pixel: Pixel, color: Color):
    return math.sqrt(sum(map(lambda x, y: (x - y) ** 2, pixel, color.rgb)))


def manhattan(pixel: RGB, color: Color):
    return sum(map(lambda x, y: abs(x - y), pixel, color.rgb))


if __name__ == "__main__":
    bit3 = range(0, 256, 0b100000)
    best = (
        min((euclidean(rgb, c), rgb, c) for c in colors)
        for rgb in product(bit3, bit3, bit3)
    )
    color_map = dict((b[1], b[2]) for b in best)
    pprint.pprint(color_map)

    with Image.open("data/example.jpeg") as img:
        w, h = img.size
        palette = defaultdict(list)

        for xy, rgb in pixel_iter(img):
            palette[rgb].append(xy)
        print("total pixels", w * h)
        print("total colors", len(palette))

    with Image.open("data/example.jpeg") as img:
        # distances = (
        #     (xy(item), p(item), c(item), euclidean(p(item), c(item)))
        #     for item in product(pixel_iter(img), colors)
        # )
        # for item in distances:
        #     print(item)
        mask = 0b11100000
        clone = img.copy()
        for xy, rgb in pixel_iter(img):
            r, g, b = rgb
            repl = color_map[(r & mask, g & mask, b & mask)]
            clone.putpixel(xy, repl.rgb)
        clone.show()
