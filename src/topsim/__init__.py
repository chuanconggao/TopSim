import re
from collections.abc import Iterable
from functools import partial
from re import Pattern

from extratools_core.dict import inverted_index
from extratools_core.str import str_to_grams

from . import setsimilarity
from .best import find_best
from .grammap import apply_gram_map, create_gram_map, update_gram_map
from .localtyping import Output, StringSet

re_split: Pattern = re.compile(r"[_\W]+", re.UNICODE)


def str_to_words(s: str) -> Iterable[str]:
    return (w for w in re_split.split(s) if len(w) > 0)


class TopSim:
    def __init__(
        self,
        s_raw_strs: Iterable[str],
        *,
        case_sensitive: bool = False,
        mapping: str = "gram",
        num_grams: int = 2,
    ) -> None:
        self._str2set_func = lambda s: {
            "gram": partial(str_to_grams, n=num_grams, pad='\0'),
            "word": str_to_words,
        }[mapping](s if case_sensitive else s.lower())

        s_raw_str_sets = [
            list(self._str2set_func(sRawStr))
            for sRawStr in s_raw_strs
        ]
        self.gramMap = create_gram_map(s_raw_str_sets)

        self.sStrs = [
            apply_gram_map(self.gramMap, sRawStrSet)
            for sRawStrSet in s_raw_str_sets
        ]
        self.sIndex = inverted_index(self.sStrs)

    def search(
        self,
        r_raw_str: str,
        *,
        k: int = 1,
        tie: bool = False,
        sim_func: str = "jaccard",
        e: float = 1 / 1000,
    ) -> Output:
        r_raw_str_set = list(self._str2set_func(r_raw_str))
        update_gram_map(self.gramMap, r_raw_str_set)

        r_str: StringSet = apply_gram_map(self.gramMap, r_raw_str_set)

        upbound_func = {
            "overlap": setsimilarity.overlap_upbound,
            "jaccard": setsimilarity.jaccard_upbound,
            "tversky": setsimilarity.tversky_upbound,
        }[sim_func]
        if sim_func == "tversky":
            setsimilarity.e = e

        return find_best(
            r_str,
            self.sStrs,
            self.sIndex,
            k=k,
            tie=tie,
            upbound_func=upbound_func,
        )
