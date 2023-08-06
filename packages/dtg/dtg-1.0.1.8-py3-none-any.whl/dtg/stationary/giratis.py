import itertools

import numpy as np


def stat(data, q=None):
    ns = data.size
    mn = np.mean(data)

    if q is None:
        q = int(np.sqrt(ns))

    dels = data - mn
    s = np.array([np.sum(dels[: i + 1]) for i in np.arange(dels.size)])
    gamma = []
    for _ in np.arange(q):
        for j in np.arange(q):
            gamma.append(np.sum(np.multiply(dels[: ns - j], dels[j:])) / ns)

    v = (np.sum(s ** 2) - (np.sum(s) ** 2 / ns)) / (ns ** 2)
    s = np.sum(gamma) / q
    if s == 0:
        return 0
    return np.abs(v / s)


def undir_stat(data, q=None, mins=True):
    ns = data.size
    mn = np.mean(data)

    if q is None:
        q = int(np.sqrt(ns))

    dels_ = data - mn
    res = []
    for dels in itertools.combinations(dels_, ns):
        dels = np.array(dels)
        s = np.array([np.sum(dels[: i + 1]) for i in np.arange(dels.size)])
        gamma = []
        for _ in np.arange(q):
            for j in np.arange(q):
                gamma.append(np.sum(np.multiply(dels[: ns - j], dels[j:])) / ns)

        v = (np.sum(s ** 2) - (np.sum(s) ** 2 / ns)) / (ns ** 2)
        s = np.sum(gamma) / q
        if s == 0:
            return 0
        res.append(np.abs(v / s))
    if mins:
        return np.min(res)
    else:
        return np.mean(res)
