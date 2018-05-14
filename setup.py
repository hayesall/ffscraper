"""
Setup file for ffscraper

As always, the setup.py sample from pypa and their walkthrough are
excellent references.

* https://packaging.python.org/tutorials/distributing-packages/
* https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here =  path.abspath(path.dirname(__file__))

# Get the long description from the README file.
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# nltk needs punkt and stopwords for ffscraper.nlp
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Import the package to read out the metadata.
import ffscraper as ffs

setup(
    # pip install ffscraper
    name=ffs.__name__,
    version=ffs.__version__,

    description='Yet another set of scraping tools for FanFiction.Net',
    long_description=long_description,
    long_description_content_type='text/markdown',

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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='fanfiction scraping search',

    project_urls={
        'Source': 'https://github.com/batflyer/FanFiction-Collaborative-Filtering',
        'Tracker': 'https://github.com/batflyer/FanFiction-Collaborative-Filtering/issues'
    },

    packages=find_packages(exclude=['docs', 'tests*'])
)
