#! /usr/bin/env python3

from .localtyping import *

from functools import partial

from .string import str2grams, str2words
from .grammap import createGramMap, updateGramMap
from .index import createIndex
from .best import findBest
from . import setsimilarity

class TopSim(object):
    def _str2set(self, s: str) -> StringSet:
        return sorted(self.gramMap[g] for g in self._str2set_func(s))


    def __init__(
            self,
            sRawStrs: RawStringSet,
            caseSensitive: bool = False,
            mapping: str = "gram", numGrams: int = 2
        ) -> None:
        self._str2set_func = lambda s: {
            "gram": partial(str2grams, n=numGrams),
            "word": str2words,
        }[mapping](s if caseSensitive else s.lower())

        self.gramMap = createGramMap(sRawStrs, self._str2set_func)

        self.sStrs = [self._str2set(line) for line in sRawStrs]
        self.sIndex = createIndex(self.sStrs)


    def search(
            self,
            rRawStr: str,
            k: int = 1, tie: bool = False,
            simFunc: str = "jaccard", e: float = 1 / 1000
        ) -> Output:
        updateGramMap(rRawStr, self._str2set_func, self.gramMap)

        rStr = self._str2set(rRawStr)

        upBoundFunc = {
            "overlap": setsimilarity.overlap_upbound,
            "jaccard": setsimilarity.jaccard_upbound,
            "tversky": setsimilarity.tversky_upbound,
        }[simFunc]
        if simFunc == "tversky":
            setsimilarity.e = e

        return findBest(rStr, self.sStrs, self.sIndex, k, tie, upBoundFunc)
