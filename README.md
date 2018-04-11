[![PyPI version](https://badge.fury.io/py/topsim.svg)](https://badge.fury.io/py/topsim)

Search the most similar strings against the query in Python 3. State-of-the-art algorithm and data structure are adopted for best efficiency. For both flexibility and efficiency, only set-based similarities are supported right now, including [Jaccard](https://en.wikipedia.org/wiki/Jaccard_index) and [Tversky](https://en.wikipedia.org/wiki/Tversky_index).

# Installation

This package is available on PyPi. Just use `pip3 install -U TopSim` to install it.

# CLI Usage

You can simply use the algorithm on terminal.

```
Usage:
    topsim-cli <query> [options] [<file>]


Options:
    -I                     Case-sensitive matching.
    -k <k>                 Maximum number of search results. [default: 1]
    --tie                  Include all the results with the same similarity of the "k"-th result. May return more than "k" results.

    -s <simfunc>           Use "jaccard", "overlap", or "tversky" as similarity function. [default: jaccard]
    -e <e>                 Parameter for "tversky" similarity. [default: 0.001]

    --mapping=<mapping>    Map each string to a set of either "gram"s or "word"s. [default: gram]
    --numgrams=<numgrams>  Number of characters for each gram when mapping by "gram". [default: 2]

    --quiet                Do not print additional information to standard error.
```

* The query is matched against each line of the input file (or standard input).

- Each line and its similarity are separated by tab character `\t`.

# API Usage

Alternatively, you can use the algorithm via API.

``` python
from topsim import TopSim

ts = TopSim([
    "python2",
    "python2.7",
    "python3",
    "python3.6",
])

print(ts.search("python", k=3)) # Return each similarity and the respective line numbers.
```

* Please check `topsim.py` for more optional parameters.

# Examples

* Search the most similar line.

`ls /usr/local/bin | ./topsim-cli "py"`

```
py	1.0
```

* Search the three most similar lines.

`ls /usr/local/bin | ./topsim-cli "py" -k 3`

```
py	1.0
py3	0.5
f2py	0.3333
```

* Use Jaccard similarity in default, which puts same weight on matching and non-matching parts.

`ls /usr/local/bin | ./topsim-cli "apple" -k 3`

```
gapplication	0.25
fpp	0.2
pphs	0.1667
```

* Use Tversky similarity, which puts more weight on matching parts.

`ls /usr/local/bin | ./topsim-cli "apple" -k 3 -s tversky`

```
x86_64-apple-darwin17.3.0-c++-7	0.9935
x86_64-apple-darwin17.3.0-g++-7	0.9935
x86_64-apple-darwin17.3.0-gcc-7	0.9935
```

# Tip
I strongly encourage using PyPy instead of CPython to run the script for best performance.
