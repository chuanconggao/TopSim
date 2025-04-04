#! /usr/bin/env python3

from typing import *

RawStringSet = List[str]
StringSet = List[int]

GramMap = Dict[str, int]

Index = Mapping[int, Sequence[Tuple[int, Sequence[int]]]]

Output = Iterable[Tuple[float, Iterable[int]]]
