#! /usr/bin/env python3

from .localtyping import *

from heapq import heappush, heappop
from collections import defaultdict

from extratools.settools import addtoset

from .setsimilarity import checkSim

def findBest(
        rStr: StringSet,
        sStrs: List[StringSet], sIndex: Index,
        k: int, tie: bool,
        upBoundFunc: Callable[[int, int, int, int, int], float]
    ) -> Output:
    worstSim = 0.0
    totalNum = 0

    simHeap: List[float] = []
    simMap: Dict[float, List[int]] = defaultdict(list)

    lnSet: Set[int] = set()
    for i, item in enumerate(rStr):
        if upBoundFunc(len(rStr), i + 1, len(rStr) - (i + 1) + 1, 1, 1) < worstSim:
            break

        for ln, p in sIndex[item]:
            if not addtoset(lnSet, ln):
                continue

            currSim = checkSim(
                worstSim, upBoundFunc,
                rStr, sStrs[ln], i + 1, p + 1, 1
            )
            if currSim is None:
                continue

            if currSim not in simMap:
                heappush(simHeap, currSim)
            simMap[currSim].append(ln)
            totalNum += 1

            if totalNum > k:
                currWorstSim = simHeap[0]
                currWorstNum = len(simMap[currWorstSim])

                if totalNum - currWorstNum >= k:
                    del simMap[currWorstSim]
                    totalNum -= currWorstNum
                    heappop(simHeap)
                elif not tie:
                    del simMap[currWorstSim][currWorstNum - (totalNum - k):]
                    totalNum = k

            if totalNum >= k:
                worstSim = simHeap[0]

    return sorted(simMap.items(), key=lambda x: x[0], reverse=True)
