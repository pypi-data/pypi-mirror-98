import numpy as np

from dtg.tail.estimate.estimator import TailEstimator


class PickandEstimator(TailEstimator):
    @staticmethod
    def get_k(x):
        return np.arange(1, int(x.size/4))

    @staticmethod
    def estimate(x, k):
        if hasattr(k, '__iter__'):
            return np.array([PickandEstimator.estimate(x, i) for i in k])

        if 4*k > x.size:
            return -1

        if x[-2*k] - x[-4*k] == 0:
            return -1
        res = (x[-k] - x[-2*k])/(x[-2*k] - x[-4*k])
        if res <= 0:
            return -1
        return np.log2(res)

    @staticmethod
    def boot_check(k, n):
        if 4*k > n:
            return int(n/4)
        return k
