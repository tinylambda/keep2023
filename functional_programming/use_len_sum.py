import math
from typing import Sequence

from base import keep_logger


def s0(samples: Sequence) -> float:
    return sum(1 for x in samples)


def s1(samples: Sequence) -> float:
    return sum(x for x in samples)


def s2(samples: Sequence) -> float:
    return sum(x * x for x in samples)


def mean(samples: Sequence) -> float:
    return s1(samples) / s0(samples)


def stdev(samples: Sequence) -> float:
    N = s0(samples)
    return math.sqrt((s2(samples) / N) - (s1(samples) / N) ** 2)


def z(x, mu_x: float, rou_x: float) -> float:
    return (x - mu_x) / rou_x


def corr(samples1: Sequence, samples2: Sequence) -> float:
    m_1, s_1 = mean(samples1), stdev(samples1)
    m_2, s_2 = mean(samples2), stdev(samples2)
    z_1 = (z(x, m_1, s_1) for x in samples1)
    z_2 = (z(x, m_2, s_2) for x in samples2)
    r = (sum(zx1 * zx2 for zx1, zx2 in zip(z_1, z_2))) / len(samples1)
    return r


if __name__ == "__main__":
    s = range(10)
    keep_logger.info("%s", mean(s))

    # data = [1, 2, 3, 4, 5]
    # s0 = len(data)
    # s1 = sum(data)
    # s2 = sum(x**2 for x in data)
    # _mean = s1 / s0
    # stdev = math.sqrt(s2 / s0 - (s1 / s0) ** 2)
    # keep_logger.info("%s", stdev)

    d = [2, 4, 4, 4, 5, 5, 7, 9]
    keep_logger.info(
        "%s",
        list(z(x, mean(d), stdev(d)) for x in d),
    )

    xi = [1.47, 1.50, 1.52]
    yi = [52.21, 53.12, 54.48]
    keep_logger.info("%s", round(corr(xi, yi), 5))
