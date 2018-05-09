"""
Setup file for ffscraper

As always, the setup.py sample from pypa and their walkthrough are
excellent references.

* https://packaging.python.org/tutorials/distributing-packages/
* https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages

# Import the package to read out the metadata.
import ffscraper as ffs

setup(
    # pip install ffscraper
    name=ffs.__name__,
    version=ffs.__version__,
    description='Yet another set of scraping tools for FanFiction.Net',
    url='https://github.com/batflyer/FanFiction-Collaborative-Filtering',

    author=ffs.__author__,
    author_email=ffs.__email__,

    license=ffs.__license__,

    classifiers=[
        # Development Information.
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',

        # Intended for research use and for the FanFiction community.
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',

        # Supported Platform.
        'Operating System :: POSIX :: Linux',

        # Supported Python Versions.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],

    keywords='fanfiction scraping search',

    project_urls={
        'Source': 'https://github.com/batflyer/FanFiction-Collaborative-Filtering',
        'Tracker': 'https://github.com/batflyer/FanFiction-Collaborative-Filtering/issues'
    },

    packages=find_packages(exclude=['docs', 'tests*'])
)
