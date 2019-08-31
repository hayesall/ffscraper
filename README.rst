#########
ffscraper
#########

|License|_ |Travis|_ |Codecov|_ |ReadTheDocs|_

.. |License| image:: https://img.shields.io/github/license/hayesall/ffscraper.svg
    :alt: License
.. _License: https://github.com/hayesall/ffscraper/blob/master/LICENSE

.. |Travis| image:: https://travis-ci.org/hayesall/ffscraper.svg?branch=master
    :alt: Travis CI continuous integration build status
.. _Travis: https://travis-ci.org/hayesall/ffscraper

.. |Codecov| image:: https://codecov.io/gh/hayesall/ffscraper/branch/master/graphs/badge.svg?branch=master
    :alt: Code coverage status
.. _Codecov: https://codecov.io/github/hayesall/ffscraper?branch=master

.. |ReadTheDocs| image:: https://readthedocs.org/projects/ffscraper/badge/?version=latest
    :alt: Documentation status
.. _ReadTheDocs: https://ffscraper.readthedocs.io/en/latest/

*Yet another set of scraping tools for FanFiction.Net*

- **Documentation**: https://ffscraper.readthedocs.io/en/latest/
- **Questions?** Contact `Alexander L. Hayes  <https://hayesall.com>`_

Getting Started
---------------

.. code-block:: bash

  pip install ffscraper

Interact with the scraper from the command line:

.. code-block:: bash

  $ python -m ffscraper --help
  $ python -m ffscraper -s 123

Or import the Python package and start building your own systems:

.. code-block:: python

  import ffscraper as ffs

  sids = ["123", "124", "125"]

  for id in sids:
    story = ffs.fanfic.story.scraper(id)
    print(story)

References
----------

.. [1] : Milli, Smitha and David Bamman, "Beyond Canonical Texts: A Computational Analysis of Fanfiction." Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing.

.. [2] : [2] Yin, K., Aragon, C., Evans, S. and Katie Davis. "Where No One Has Gone Before: A Meta-Dataset of the World's Largest Fanfiction Repository." Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems. ACM, 2017.

Attribution
-----------

- [monochrome](https://github.com/dyutibarma/monochrome) is a Jekyll theme by [@dyutibarma](https://github.com/dyutibarma/). Used under the terms of the [MIT License](https://github.com/dyutibarma/monochrome/blob/master/license.md).
