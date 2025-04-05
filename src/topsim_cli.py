#! /usr/bin/env python3

"""
Usage:
    topsim-cli <query> [options] [<file>]

    topsim-cli --help


Options:
    -I                     Case-sensitive matching.
    -k <k>                 Maximum number of search results. [default: 1]
    --tie                  Include all the results with the same similarity of the "k"-th result. May return more than "k" results.

    -s, --search           Search the query within each line rather than against the whole line, by preferring partial matching of the line.
                           Tversky similarity is used instead of Jaccard similarity.
    -e <e>                 Parameter for Tversky similarity. [default: 0.001]

    --mapping=<mapping>    Map each string to a set of either "gram"s or "word"s. [default: gram]
    --numgrams=<numgrams>  Number of characters for each gram when mapping by "gram". [default: 2]

    --quiet                Do not print additional information to standard error.
"""  # noqa: E501

import os
import sys
from functools import partial
from typing import cast

from docopt import ParsedOptions, docopt
from extratools_core.debug import peakmem, stopwatch

from topsim import TopSim
from topsim.localtyping import Output

argv: ParsedOptions = docopt(cast("str", __doc__))

print2 = partial(
    print,
    file=(
        open(os.devnull, 'w', encoding='utf-8') if argv["--quiet"]
        else sys.stderr
    ),
)


def print_resource_usage() -> None:
    print2(f"{stopwatch() * 1_000:.2f} ms | {peakmem() / 1024 / 1024 / 1024:.2f} KB")


stopwatch()


s_raw_strs = [
    line.rstrip('\r\n')
    for line in (open(argv["<file>"]) if argv["<file>"] else sys.stdin)
]

print2("Indexing...", end=" ")

ts = TopSim(
    s_raw_strs,
    case_sensitive=argv["-I"],
    mapping=argv["--mapping"],
    num_grams=int(argv["--numgrams"]),
)

print_resource_usage()

print2("Searching...", end=" ")

r_best: Output = ts.search(
    argv["<query>"],
    k=int(argv["-k"]),
    tie=argv["--tie"],
    sim_func="tversky" if argv["--search"] else "jaccard",
    e=float(argv["-e"]),
)

print_resource_usage()

print2()

for sim, lns in r_best:
    for ln in lns:
        print(f"{s_raw_strs[ln]}\t{sim:.4}")


# Placeholder function for pyproject.toml requirement of scripts
def run():
    pass
