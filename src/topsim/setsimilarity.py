from collections.abc import Callable

from extratools_core.math import safediv

from .localtyping import StringSet

__numStepForBound = 10


def check_sim(
    bound: float,
    upbound_func: Callable[[int, int, int, int, int], float],
    a: StringSet,
    b: StringSet,
    i: int = 0,
    j: int = 0,
    count: int = 0,
) -> float | None:
    la, lb = len(a), len(b)

    if bound > upbound_func(la, i, lb, j, count):
        return None

    step = 0
    while i < la and j < lb:
        x = a[i]
        y = b[j]

        if x < y:
            i += 1
        elif x > y:
            j += 1
        else:
            i += 1
            j += 1
            count += 1

        step += 1
        if step % __numStepForBound == 0 and bound > upbound_func(la, i, lb, j, count):
            return None

    sim = upbound_func(la, i, lb, j, count)
    return None if bound > sim else sim


def overlap_upbound(a_len: int, a_passed: int, b_len: int, b_passed: int, count: int) -> float:
    return count + min(a_len - a_passed, b_len - b_passed)


def jaccard_upbound(a_len: int, a_passed: int, b_len: int, b_passed: int, count: int) -> float:
    max_count = overlap_upbound(**locals())
    return min(
        1.0,
        safediv(max_count, a_len + b_len - max_count),
    )


# Assume all sets are shorter than 1 / e
e = 1 / 1000


def tversky_upbound(a_len: int, a_passed: int, b_len: int, b_passed: int, count: int) -> float:
    return min(
        1.0,
        safediv(
            overlap_upbound(**locals()),
            (1 - e) * a_len + e * b_len,
        ),
    )
