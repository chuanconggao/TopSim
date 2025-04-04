#! /usr/bin/env python3

from .localtyping import *

from collections import Counter
from itertools import count

def createGramMap(
        sRawStrSets: Iterable[RawStringSet],
    ) -> GramMap:
    gramFreqs: Counter = Counter()

    for sRawStrSet in sRawStrSets:
        gramFreqs.update(sRawStrSet)

    gramMapper = count(start=0)

    return {
        gram: next(gramMapper)
        for gram, _ in sorted(
            gramFreqs.items(),
            key=lambda x: (x[1], x[0])
        )
    }


def updateGramMap(
        gramMap: GramMap,
        rRawStrSet: RawStringSet
    ) -> None:
    gramMapper = count(start=-1, step=-1)

    gramMap.update(
        (gram, next(gramMapper))
        for gram in rRawStrSet
        if gram not in gramMap
    )


def applyGramMap(
        gramMap: GramMap,
        rRawStrSet: RawStringSet
    ) -> StringSet:
    return sorted(gramMap[gram] for gram in rRawStrSet)
