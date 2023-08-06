import numpy as np
from scipy.special import erfinv


def estimate_t_p(val):
    return erfinv(2*val-1)*np.sqrt(2)


def estimate_ro_p(val):
    return erfinv(1-val)*np.sqrt(2)


def boot(entity, x, alp, beta, num, k, real=None):
    if hasattr(k, "__iter__"):
        if len(k) == 0:
            return [(np.infty, -1, [])]

        return np.array([boot(entity, x, alp, beta, num, i, entity.estimate(x, i)) for i in k if entity.estimate(x, i) != -1])

    if real is None:
        real = entity.estimate(x, k)
    if real == -1:
        return (np.infty, -1, [])

    try:
        k1 = int(k / (x.size ** ((1 - beta) * alp)))
        n1 = int(x.size ** beta)
        k1 = entity.boot_check(k1, n1)

        ga = []
        while len(ga) < num:
            sub_x = np.array(
                [x[i] for i in np.random.choice(x.size, n1, replace=True)]
            )
            sub_x.sort()
            rsi = entity.estimate(sub_x, k1)
            if rsi == -1:
                continue

            ga.append(rsi)

        ga = np.array(ga)
        bias = (np.mean(ga) - real) ** 2
        vr = np.var(ga)

        return vr + bias, real, ga
    except Exception as error:
        print(error)
        return np.infty, -1, []
    except OverflowError as error:
        print(error)
        return np.infty, -1, []

# alp = 2/3, beta = 1/2 for Hill's estimator
def boot_estimate(entity, x, alp, beta, num, pers=(0.95, 0.025), qt=0.05, back=True):
    k = entity.get_k(x, boot=True)
    x_ = entity.prepare(x)

    if len(k) < 2:
        return -1, (0, 0)

    t_p = estimate_t_p(pers[0])
    ro_p = estimate_ro_p(pers[1])
    ro = ro_p * (1 + (t_p / np.sqrt(2 * num) + ((5 * (t_p ** 2) + 10) / (12 * num))))
    mses, alps, dls = zip(*boot(entity, x_, alp, beta, num, k, ro))

    ar = np.argmin(mses)
    dls = dls[ar]

    if back:
        mn = np.mean(dls)
        mn2 = np.mean(1/dls)
        ds = np.var(dls)
        return (
            1/alps[ar],
            (
                mn2 - ro * np.sqrt(ds*mn2/mn),
                mn2 + ro * np.sqrt(ds*mn2/mn),
            ),
            (
                np.quantile(1/dls, qt),
             np.quantile(1/dls, 1-qt)
            )
        )
    else:
        return (
            alps[ar],
            (
                np.mean(dls) - ro * np.std(dls),
                np.mean(dls) + ro * np.std(dls),
            ),
            (
                np.quantile(dls, qt),
                np.quantile(dls, 1-qt)
            )
        )
