import numpy as np


def optimal_value(x, entity):
    x_ = entity.prepare(x)
    ks = entity.get_k(x_)

    sles = []
    for k in ks:
        i_s = np.arange(x_.size - k + 1, x_.size)

        if i_s.size < 3:
            continue

        xs = - np.log([1 - (i/(x_.size+1)) for i in i_s])
        ys = np.log([x_[- x_.size + i - 1] for i in i_s])
        covs = np.cov(xs, ys)
        sles.append(covs[0][1]/covs[0][0])
    return entity.estimate(x_, ks[-1])
