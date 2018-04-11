#! /usr/bin/env python3

from .localtyping import *

import re

def str2grams(s: str, n: int) -> RawStringSet:
    return [
        s[i:i + n] for i in range(len(s) - n + 1)
    ] if len(s) >= n else [s]


reSplit = re.compile(r"[_\W]+", re.U)
def str2words(s: str) -> RawStringSet:
    return [w for w in reSplit.split(s) if len(w) > 0]
