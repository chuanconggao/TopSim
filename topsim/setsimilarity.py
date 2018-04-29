#! /usr/bin/env python3

from .localtyping import *

from extratools.mathtools import safediv

numStepForBound = 10

def checkSim(
        bound: float,
        upBoundFunc: Callable[[int, int, int, int, int], float],
        a: StringSet, b: StringSet,
        i: int = 0, j: int = 0, count: int = 0
    ):
    la, lb = len(a), len(b)

    if bound > upBoundFunc(la, i, lb, j, count):
        return None

    step = 0
    while i < la and j < lb:
        x = a[i]
        y = b[j]

        if x < y:
            i += 1
            #  if bound > upBoundFunc(la, i, lb, j, count):
                #  return None
        elif x > y:
            j += 1
            #  if bound > upBoundFunc(la, i, lb, j, count):
                #  return None
        else:
            i += 1
            j += 1
            count += 1

        step += 1
        if step % numStepForBound == 0:
            if bound > upBoundFunc(la, i, lb, j, count):
                return None

    sim = upBoundFunc(la, i, lb, j, count)
    return None if bound > sim else sim


def overlap_upbound(aLen: int, aPassed: int, bLen: int, bPassed: int, count: int):
    return count + min(aLen - aPassed, bLen - bPassed)


def jaccard_upbound(aLen: int, aPassed: int, bLen: int, bPassed: int, count: int):
    maxCount = overlap_upbound(**locals())
    return min(
        1.0,
        safediv(maxCount, aLen + bLen - maxCount)
    )


# Assume all sets are shorter than 1 / e
e = 1 / 1000

def tversky_upbound(aLen: int, aPassed: int, bLen: int, bPassed: int, count: int):
    return min(
        1.0,
        safediv(
            overlap_upbound(**locals()),
            (1 - e) * aLen + e * bLen
        )
    )
