from collections import defaultdict
from collections.abc import Callable
from heapq import heappop, heappush

from extratools_core.set import add_to_set

from .localtyping import Index, Output, StringSet
from .setsimilarity import check_sim


def find_best(
    r_str: StringSet,
    s_strs: list[StringSet],
    s_index: Index,
    *,
    k: int,
    tie: bool,
    upbound_func: Callable[[int, int, int, int, int], float],
) -> Output:
    worst_sim: float = 0.0
    total_num: int = 0

    sim_heap: list[float] = []
    sim_map: dict[float, list[int]] = defaultdict(list)

    ln_set: set[int] = set()
    for i, item in enumerate(r_str):
        if upbound_func(len(r_str), i + 1, len(r_str) - (i + 1) + 1, 1, 1) < worst_sim:
            break

        for ln, p in s_index[item]:
            if not add_to_set(ln_set, ln):
                continue

            curr_sim: float | None = check_sim(
                worst_sim,
                upbound_func,
                r_str,
                s_strs[ln],
                i + 1,
                p[0] + 1,
                1,
            )
            if curr_sim is None:
                continue

            if curr_sim not in sim_map:
                heappush(sim_heap, curr_sim)
            sim_map[curr_sim].append(ln)
            total_num += 1

            if total_num > k:
                curr_worst_sim: float = sim_heap[0]
                curr_worst_num: int = len(sim_map[curr_worst_sim])

                if total_num - curr_worst_num >= k:
                    del sim_map[curr_worst_sim]
                    total_num -= curr_worst_num
                    heappop(sim_heap)
                elif not tie:
                    del sim_map[curr_worst_sim][curr_worst_num - (total_num - k):]
                    total_num = k

            if total_num >= k:
                worst_sim = sim_heap[0]

    return sorted(sim_map.items(), key=lambda x: x[0], reverse=True)
