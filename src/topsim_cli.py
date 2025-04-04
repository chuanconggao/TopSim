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
"""

import sys
from functools import partial
import os

from docopt import docopt
from extratools.debugtools import stopwatch, peakmem

from topsim import TopSim

argv = docopt(__doc__)

print2 = partial(print, file=(open(os.devnull, 'w') if argv["--quiet"] else sys.stderr))

def printResourceUsage():
    print2("{:.2} sec | {:.2} MB".format(
        stopwatch()[1],
        peakmem() / 1024 / 1024
    ))


sRawStrs = [
    line.rstrip('\r\n')
    for line in (open(argv["<file>"]) if argv["<file>"] else sys.stdin)
]

print2("Indexing...", end=" ")

ts = TopSim(
    sRawStrs,
    argv["-I"],
    mapping=argv["--mapping"],
    numGrams=int(argv["--numgrams"])
)

printResourceUsage()

print2("Searching...", end=" ")

rBest = ts.search(
    argv["<query>"],
    int(argv["-k"]),
    argv["--tie"],
    "tversky" if argv["--search"] else "jaccard",
    float(argv["-e"])
)

printResourceUsage()

print2()

for sim, lns in rBest:
    for ln in lns:
        print("{}\t{:.4}".format(sRawStrs[ln], sim))


# Placeholder function for pyproject.toml requirement of scripts
def run():
    pass
