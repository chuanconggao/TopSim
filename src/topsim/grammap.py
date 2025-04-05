from collections import Counter
from collections.abc import Iterable
from itertools import count

from .localtyping import GramMap, RawStringSet, StringSet


def create_gram_map(
    s_raw_str_sets: Iterable[RawStringSet],
) -> GramMap:
    gram_freqs: Counter = Counter()

    for s_raw_str_set in s_raw_str_sets:
        gram_freqs.update(s_raw_str_set)

    gram_mapper = count(start=0)

    return {
        gram: next(gram_mapper)
        for gram, _ in sorted(
            gram_freqs.items(),
            key=lambda x: (x[1], x[0]),
        )
    }


def update_gram_map(
    gram_map: GramMap,
    r_raw_str_set: RawStringSet,
) -> None:
    gram_mapper = count(start=-1, step=-1)

    gram_map.update(
        (gram, next(gram_mapper))
        for gram in r_raw_str_set
        if gram not in gram_map
    )


def apply_gram_map(
    gram_map: GramMap,
    r_raw_str_set: RawStringSet,
) -> StringSet:
    return sorted(gram_map[gram] for gram in r_raw_str_set)
