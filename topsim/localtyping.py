#! /usr/bin/env python3

from typing import *

RawStringSet = List[str]
StringSet = List[int]

MappingFunc = Callable[[str], RawStringSet]

GramMap = Dict[str, int]

Index = Dict[int, List[Tuple[int, int]]]

Output = Iterable[Tuple[float, Iterable[int]]]
