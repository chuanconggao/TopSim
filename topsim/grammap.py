#! /usr/bin/env python3

from .localtyping import *

from collections import Counter

from .remapper import Remapper

def createGramMap(
        sRawStrSets: Iterable[RawStringSet],
    ) -> GramMap:
    gramFreqs = Counter()

    for sRawStrSet in sRawStrSets:
        gramFreqs.update(sRawStrSet)

    gramMapper = Remapper()

    return {
        gram: gramMapper.next()
        for gram, _ in sorted(
            gramFreqs.items(),
            key=lambda x: (x[1], x[0])
        )
    }


def updateGramMap(
        gramMap: GramMap,
        rRawStrSet: RawStringSet
    ) -> None:
    gramMapper = Remapper(start=-1, step=-1)

    gramMap.update(
        (gram, gramMapper.next())
        for gram in rRawStrSet
        if gram not in gramMap
    )


def applyGramMap(
        gramMap: GramMap,
        rRawStrSet: RawStringSet
    ) -> StringSet:
    return sorted(gramMap[gram] for gram in rRawStrSet)
