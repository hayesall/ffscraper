ffscraper
=========

  *Yet another Python package for scraping FanFiction.Net...*

  ``pip install ffscraper``

  :Authors:
     `Alexander L. Hayes <https://hayesall.com>`_

  :Version: 0.2.0

  :Documentation: :ref:`modindex`
  :Search: :ref:`search`

  :Source: `GitHub <https://github.com/hayesall/ffscraper/>`_
  :Bugtracker: `GitHub Issues <https://github.com/hayesall/ffscraper/issues/>`_

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

FanFiction.Net was established in 1998 and is among the world's largest
collection of user-submitted fanfiction (works of fanfiction authored by fans
of existing stories; such as movies, books, or TV shows).  Recently the large
amount of easily-available user content has drawn interest in analyzing the
content and creative differences between original works and their fanfiction
counterparts [#]_, and [#]_ created an anonymized dataset of the metadata.

This project is twofold: creating open-source systems for scraping content,
and using that content to build open-source systems which can be used by the
FanFiction.Net community.

Installation and Usage
======================

Interact with the scraper from the commandline:

.. code-block:: bash

		$ pip install ffscraper
		$ python -m ffscraper --help
		$ python -m ffscraper -s 123

Or import the Python package and start building your own systems:

.. code-block:: python

		import ffscraper as ffs

		sids = ['123', '124', '125']

		for id in sids:
		    story = ffs.fanfic.story.scraper(id)
		    print(story)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ffscraper.rst

.. [#] Milli, Smitha and David Bamman, "Beyond Canonical Texts: A Computational Analysis of Fanfiction." Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing.
.. [#] Yin, K., Aragon, C., Evans, S. and Katie Davis. "Where No One Has Gone Before: A Meta-Dataset of the World's Largest Fanfiction Repository." Proceedings of the 2017 CHI Conference on Human Factors in Computing Systems. ACM, 2017.
