#! /usr/bin/env python3

from .localtyping import *

from heapq import heappush, heappop
from collections import defaultdict

from .setsimilarity import checkSim

def __addToSet(s: Set[Any], x: Any) -> bool:
    if x in s:
        return False

    s.add(x)
    return True


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

        if item not in sIndex or i > 0 and item == rStr[i - 1]:
            continue

        for ln, p in sIndex[item]:
            if not __addToSet(lnSet, ln):
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
                    totalNum -= currWorstNum
                    heappop(simHeap)
                    del simMap[currWorstSim]

            if totalNum >= k:
                worstSim = simHeap[0]

            if not tie and totalNum > k:
                currWorstNum = len(simMap[worstSim]) - (totalNum - k)
                del simMap[worstSim][currWorstNum:]
                totalNum = k


    return sorted(simMap.items(), key=lambda x: x[0], reverse=True)
