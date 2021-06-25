import numpy as np
import numpy.typing as npt


# There also is
# <https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html>,
# but implementation is easy enough
def _logsumexp(x):
    c = np.max(x)
    return c + np.log(np.sum(np.exp(x - c)))


def mean(x: npt.ArrayLike, p: float = 1):
    x = np.asarray(x)

    n = len(x)
    if p == 1:
        return np.mean(x)
    if p == -np.inf:
        return np.min(np.abs(x))
    elif p == 0:
        # first compute the root, then the product, to avoid numerical difficulties with
        # too small values of prod(x)
        if np.any(x < 0.0):
            raise ValueError("p=0 only works with nonnegative x.")
        return np.prod(np.power(x, 1 / n))
    elif p == np.inf:
        return np.max(np.abs(x))

    if not isinstance(p, int) and np.any(x < 0.0):
        raise ValueError("Non-integer p only work with nonnegative x.")

    if np.all(x > 0.0):
        # logsumexp trick to avoid overflow for large p
        # only works for positive x though
        return np.exp((_logsumexp(p * np.log(x)) - np.log(n)) / p)
    else:
        return (np.sum(x ** p) / n) ** (1.0 / p)
