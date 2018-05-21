.. ffscraper documentation master file, created by
   sphinx-quickstart on Wed May  9 16:53:06 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ffscraper
=========

  *Yet another Python package for scraping FanFiction.Net...*

  ``pip install ffscraper``

  :Authors:
     Alexander L. Hayes (`@batflyer <https://github.com/batflyer/>`_)

  :Version: 0.2.0

  :Documentation: :ref:`modindex`
  :Search: :ref:`search`

  :Source: `GitHub <https://github.com/batflyer/FanFiction-Collaborative-Filtering/>`_
  :Bugtracker: `GitHub Issues <https://github.com/batflyer/FanFiction-Collaborative-Filtering/issues/>`_

  .. image:: https://img.shields.io/pypi/pyversions/ffscraper.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/v/ffscraper.svg?style=flat-square
  .. image:: https://img.shields.io/pypi/l/ffscraper.svg?style=flat-square
  .. image:: https://codecov.io/gh/batflyer/FanFiction-Collaborative-Filtering/branch/master/graph/badge.svg?token=psUEAhqaGl
  .. image:: https://img.shields.io/readthedocs/fanfiction-collaborative-filtering/stable.svg?style=flat-square

FanFiction.Net was established in 1998 and is among the world's largest collection of user-submitted fanfiction (works of fanfiction authored by fans of existing stories; such as movies, books, or TV shows).  Recently the large amount of easily-available user content has drawn interest in analyzing the content and creative differences between original works and their fanfiction counterparts [#]_, and [#]_ created an anonymized dataset of the metadata.

This project is twofold: creating open-source systems for scraping content, and using that content to build open-source systems which can be used by the FanFiction.Net community.

Installation and Usage
======================

Interact with the scraper from the commandline:

.. code-block:: bash

		$ pip install ffscraper
		$ python -m ffscraper --help
		$ python -m ffscraper -s 123

Or import the Python package and start building your own systems:

.. code-block:: python

		from __future__ import print_function
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
