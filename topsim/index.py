#! /usr/bin/env python3

from .localtyping import *

from collections import defaultdict

def createIndex(sStrs: List[StringSet]) -> Index:
    sIndex: Index = defaultdict(list)

    for (i, sStr) in enumerate(sStrs):
        for (p, item) in enumerate(sStr):
            if p > 0 and item == sStr[p - 1]:
                continue

            sIndex[item].append((i, p))

    return sIndex
