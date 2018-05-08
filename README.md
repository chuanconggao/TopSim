[![PyPI version](https://img.shields.io/pypi/v/TopSim.svg)](https://pypi.python.org/pypi/TopSim/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/TopSim.svg)](https://pypi.python.org/pypi/TopSim/)
[![PyPI license](https://img.shields.io/pypi/l/TopSim.svg)](https://pypi.python.org/pypi/TopSim/)

Search the most similar strings against the query in Python 3. State-of-the-art algorithm and data structure are adopted for best efficiency. For both flexibility and efficiency, only set-based similarities are supported right now, including [Jaccard](https://en.wikipedia.org/wiki/Jaccard_index) and [Tversky](https://en.wikipedia.org/wiki/Tversky_index).

- For simpler code, some general purpose functions have been moved to be part of a new library [extratools](https://github.com/chuanconggao/extratools).

- [TopEmoji](https://github.com/chuanconggao/TopEmoji) is an interesting application of this library, searching the most similar emojis against the query.

``` bash
topemoji-cli "baby" -k 5
```

``` text
👶	baby	1.0
👼	baby angel	0.666
🐤	baby chick	0.666
🍼	baby bottle	0.6659
🚼	baby symbol	0.6659
```

# Installation

This package is available on PyPI. Just use `pip3 install -U TopSim` to install it.

# CLI Usage

You can simply use the algorithm on terminal.

```
Usage:
    topsim-cli <query> [options] [<file>]


Options:
    -I                     Case-sensitive matching.
    -k <k>                 Maximum number of search results. [default: 1]
    --tie                  Include all the results with the same similarity of the "k"-th result. May return more than "k" results.

    -s, --search           Search the query within each line rather than against the whole line, by preferring partial matching of the line.
                           Tversky similarity is used instead of Jaccard similarity.
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

* Please check `topsim.py` for more optional parameters, like similarity function, etc.

# Examples

* Search the most similar line.

`ls /usr/bin | topsim-cli "top"`

```
top	1.0
```

* Search the three most similar lines.

`ls /usr/bin | topsim-cli "top" -k 3`

```
top	1.0
tops	0.5
iotop	0.4286
```

* Use Jaccard similarity in default, which puts same weight on matching both the query and the lines.

`ls /usr/bin | topsim-cli "git" -k 5`

```
git	1.0
wait	0.2857
git-shell	0.2727
pluginkit	0.2727
kinit	0.25
```

* Use Tversky similarity, which puts most weight on matching the query. Ideal when searching within long lines.

`ls /usr/bin | topsim-cli "git" -k 5 -s`

```
git	1.0
git-shell	0.7489
pluginkit	0.7489
git-cvsserver	0.7481
git-upload-pack	0.7478
```

- For `n`-gram mapping, higher number of `n` for can result in better accuracy but fewer matches.

`ls /usr/bin | topsim-cli "git" -k 5 -s --numgrams=3`

```
git	1.0
git-shell	0.5993
git-cvsserver	0.5988
git-upload-pack	0.5986
git-receive-pack	0.5984
```

- Full support of Chinese/Japanese/Korean.

`cat test`

``` text
地三鲜
红烧肉
烤全牛
木须肉
土豆炖牛肉
```

`cat test | topsim-cli "牛肉" -k 3 -s`

``` text
土豆炖牛肉	0.666
红烧肉	0.3332
木须肉	0.3332
```

# Tip
I strongly encourage using PyPy instead of CPython to run the script for best performance.
