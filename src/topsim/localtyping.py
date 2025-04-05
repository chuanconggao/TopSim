from collections.abc import Iterable, Mapping, Sequence

RawStringSet = list[str]
StringSet = list[int]

GramMap = dict[str, int]

Index = Mapping[int, Sequence[tuple[int, Sequence[int]]]]

Output = Iterable[tuple[float, Iterable[int]]]
