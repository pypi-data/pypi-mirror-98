import numpy as np


class TailEstimator:
    @staticmethod
    def prepare(x):
        return np.sort(x)

    @staticmethod
    def get_k(x, boot=False):
        if boot:
            return np.arange(int(x.size/40), int(x.size/2))
        return np.arange(2, x.size-2)

    @staticmethod
    def estimate(x, k):
        return None

    @staticmethod
    def boot_check(k, n):
        if k + 1 > n:
            return n - 1
        return k

    @staticmethod
    def get_opt_k(x):
        return None
