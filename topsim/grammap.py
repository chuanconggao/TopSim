#! /usr/bin/env python3

from .localtyping import *

from collections import Counter

from .remapper import Remapper

def createGramMap(
        sRawStrs: Iterable[str],
        str2set_func: MappingFunc
    ) -> GramMap:
    gramFreqs = Counter()

    for line in sRawStrs:
        gramFreqs.update(str2set_func(line))

    gramMapper = Remapper()

    return {
        g: gramMapper.next()
        for g, _ in sorted(
            gramFreqs.items(),
            key=lambda x: (x[1], x[0])
        )
    }


def updateGramMap(
        rRawStr: str,
        str2set_func: MappingFunc,
        gramMap: GramMap
    ) -> None:
    gramMapper = Remapper(start=-1, step=-1)

    gramMap.update(
        (g, gramMapper.next())
        for g in str2set_func(rRawStr)
        if g not in gramMap
    )
