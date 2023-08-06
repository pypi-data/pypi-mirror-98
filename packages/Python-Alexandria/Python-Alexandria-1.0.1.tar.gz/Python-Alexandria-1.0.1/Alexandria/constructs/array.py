import numpy as np
from math import ceil


def find_nearest_entry(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]


def min_multiple_under(x, base):
    """
    :param x: Maximum value
    :param base: Base
    :return: Minimum multiple of Base larger than x
    """
    return base*ceil(x/base)


def span(a):
    a_s = a + a.min() if a.min() < 0 else a
    return max(a_s) - min(a_s)


def dx_v(t):
    """
    :return: Return vector of base dimension increments, where the base dimension is X in
                    f(X)
             for higher precision differentiation or integration with uneven measurements.
    """
    dt_v = np.array(list([t[i + 1] - t[i]] for i in range(t.size - 1)))
    dt_v = np.append(dt_v, np.array([t[-2] - t[-1]]))
    return dt_v
