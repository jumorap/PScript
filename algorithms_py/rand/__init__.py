import math


MODLUS = 2147483647
MULT1 = 24112
MULT2 = 26143
zrng = [1,
        1973272912, 281629770, 20006270, 1280689831, 2096730329, 1933576050,
        913566091, 246780520, 1363774876, 604901985, 1511192140, 1259851944,
        824064364, 150493284, 242708531, 75253171, 1964472944, 1202299975,
        233217322, 1911216000, 726370533, 403498145, 993232223, 1103205531,
        762430696, 1922803170, 1385516923, 76271663, 413682397, 726466604,
        336157058, 1432650381, 1120463904, 595778810, 877722890, 1046574445,
        68911991, 2088367019, 748545416, 622401386, 2122378830, 640690903,
        1774806513, 2132545692, 2079249579, 78130110, 852776735, 1187867272,
        1351423507, 1645973084, 1997049139, 922510944, 2045512870, 898585771,
        243649545, 1004818771, 773686062, 403188473, 372279877, 1901633463,
        498067494, 2087759558, 493157915, 597104727, 1530940798, 1814496276,
        536444882, 1663153658, 855503735, 67784357, 1432404475, 619691088,
        119025595, 880802310, 176192644, 1116780070, 277854671, 1366580350,
        1142483975, 2026948561, 1053920743, 786262391, 1792203830, 1494667770,
        1923011392, 1433700034, 1244184613, 1147297105, 539712780, 1545929719,
        190641742, 1645390429, 264907697, 620389253, 1502074852, 927711160,
        364849192, 2049576050, 638580085, 547070247]


def lcgrand(num):
    """
    Return a random number between 0 and 1 with seed num using the linear congruential generator method.
    :param num: seed number
    """
    num = num % len(zrng)
    zi = zrng[num]
    lowprd = (zi & 65535) * MULT1
    hi31 = (zi >> 16) * MULT1 + (lowprd >> 16)
    zi = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODLUS
    lowprd = (zi & 65535) * MULT2
    hi31 = (zi >> 16) * MULT2 + (lowprd >> 16)
    zi = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
        zi += MODLUS
    zrng[num] = zi
    return float(zi >> 7 | 1) / 16777216.0


def exponential_distribution(seed, lambda_value):
    u = lcgrand(lambda_value)
    return -math.log(u) / lambda_value


def geometric_distribution(seed, p):
    u = lcgrand(seed)
    return math.log(1 - u) / math.log(1 - p)


def normal_distribution(seed, mu, sigma):
    u1 = lcgrand(seed)
    u2 = lcgrand(seed + 1)
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    x = mu + sigma * z0
    return x


def poisson_distribution(seed, lambda_value):
    l = math.exp(-lambda_value)
    k = 0
    p = 1.0

    while p > l:
        k += 1
        u = lcgrand(seed + k)
        p *= u

    return k - 1


def uniform_distribution(seed, a, b):
    u = lcgrand(seed)
    x = a + (b - a) * u
    return x


def exponential_distribution_list(num, lamda, n):
    return [exponential_distribution(num, lamda) for _ in range(n)]


def geometric_distribution_list(seed, num, n):
    return [geometric_distribution(seed, num) for _ in range(n)]


def normal_distribution_list(seed, mu, sigma, n):
    return [normal_distribution(seed, mu, sigma) for _ in range(n)]


def poisson_distribution_list(seed, lambda_value, n):
    return [poisson_distribution(seed, lambda_value) for _ in range(n)]


def uniform_distribution_list(seed, a, b, n):
    return [uniform_distribution(seed, a, b) for _ in range(n)]
