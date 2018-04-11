#! /usr/bin/env python3

from .localtyping import *

from functools import partial

from .str2set import str2grams, str2words
from .grammap import createGramMap, updateGramMap, applyGramMap
from .index import createIndex
from .best import findBest
from . import setsimilarity

class TopSim(object):
    def __init__(
            self,
            sRawStrs: Iterable[str],
            caseSensitive: bool = False,
            mapping: str = "gram", numGrams: int = 2
        ) -> None:
        self._str2set_func = lambda s: {
            "gram": partial(str2grams, n=numGrams),
            "word": str2words,
        }[mapping](s if caseSensitive else s.lower())

        sRawStrSets = [
            self._str2set_func(sRawStr)
            for sRawStr in sRawStrs
        ]
        self.gramMap = createGramMap(sRawStrSets)

        self.sStrs = [
            applyGramMap(self.gramMap, sRawStrSet)
            for sRawStrSet in sRawStrSets
        ]
        self.sIndex = createIndex(self.sStrs)


    def search(
            self,
            rRawStr: str,
            k: int = 1, tie: bool = False,
            simFunc: str = "jaccard", e: float = 1 / 1000
        ) -> Output:
        rRawStrSet = self._str2set_func(rRawStr)
        updateGramMap(self.gramMap, rRawStrSet)

        rStr = applyGramMap(self.gramMap, rRawStrSet)

        upBoundFunc = {
            "overlap": setsimilarity.overlap_upbound,
            "jaccard": setsimilarity.jaccard_upbound,
            "tversky": setsimilarity.tversky_upbound,
        }[simFunc]
        if simFunc == "tversky":
            setsimilarity.e = e

        return findBest(rStr, self.sStrs, self.sIndex, k, tie, upBoundFunc)
