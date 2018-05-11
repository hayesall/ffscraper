# Collaborative Filtering in FanFiction Networks

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ffscraper.svg?style=flat-square) ![PyPI](https://img.shields.io/pypi/v/ffscraper.svg?style=flat-square) ![license](https://img.shields.io/pypi/l/ffscraper.svg?style=flat-square) [![Read the Docs (version)](https://img.shields.io/readthedocs/fanfiction-collaborative-filtering/stable.svg?style=flat-square)](http://fanfiction-collaborative-filtering.readthedocs.io/en/latest/)

*Yet another set of scraping tools for FanFiction.Net*

**Alexander L. Hayes** ([@batflyer](https://github.com/batflyer))

FanFiction.Net was established in 1998 and is among the world's largest collection of user-submitted fanfiction (works of fiction authored by fans of existing stories, such as movies, books, or TV shows). The large amount of easily-available user content has drawn interest from those interested in analyzing the content and creative differences between original works and their fanfiction derivatives [1]. More recently, [2] created an anonymized dataset of the metadata from fanfiction sources.

This repository's purpose is twofold: creating robust open-source tools for scraping content, and using that content to build open-source systems which can be used by the FanFiction.Net community.

### Docs and Installation

Full documentation on [readthedocs](http://fanfiction-collaborative-filtering.readthedocs.io/en/latest/).

From PyPi:

```
pip install ffscraper
```

From GitHub:

```
pip install git+git://github.com/batflyer/FanFiction-Collaborative-Filtering.git
```

### Quick-Start

Interact with the scraper from the commandline:

```bash
$ pip install ffscraper
$ python -m ffscraper --help
$ python -m ffscraper -s 123
```

Or import the Python package and start building your own systems:

```python
from __future__ import print_function
import ffscraper as ffs

sids = ['123', '124', '125']

for id in sids:
    story = ffs.fanfic.story.scraper(id)
    print(story)
```

### References

* [1] Milli, Smitha and David Bamman, "Beyond Canonical Texts: A Computational Analysis of Fanfiction." Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing.
* [2] Yin, K., Aragon, C., Evans, S. and Katie Davis. "Where No One Has Gone Before: A Meta-Dataset of the World's Largest Fanfiction Repository." Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems. ACM, 2017.

### Attribution

* This was originally part of a final project for Professor Vibhav Gogate's Spring 2018 [Advanced Machine Learning](http://www.hlt.utdallas.edu/~vgogate/ml/2018s/index.html) class at the University of Texas at Dallas. This version of the code, TeX, and .pdf are tagged as v0.1.0.
* [monochrome](https://github.com/dyutibarma/monochrome) is a Jekyll theme by [@dyutibarma](https://github.com/dyutibarma/). Used under the terms of the [MIT License](https://github.com/dyutibarma/monochrome/blob/master/license.md).
