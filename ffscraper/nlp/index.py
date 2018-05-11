
#   Copyright (c) 2018 Alexander L. Hayes (@batflyer)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
+---------------------+-----------------------------+
|     **Name**        |       **Description**       |
+---------------------+-----------------------------+
| ffscraper.nlp.index | A module for indexing text. |
+---------------------+-----------------------------+

As text is read from FanFiction.Net, it would be useful to have some method
for automatically analyzing, storing, and (inevitably) retrieving the data
in a systematized way.

This method helps to accomplish this by creating an inverted index from
text passed into it, regardless of whether the text was originally from a
story, profile, or a story review.

.. note:: This currently assumes that the text passed into it is in English.
   As this increases in complexity there should be a way to stem and index
   words in their respective language (especially since Spanish, French,
   Indonesian, and a large handful of non-English languages are quite common).

"""

from __future__ import print_function

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *

_stemmer = PorterStemmer()
_stopwords = stopwords.words('english')

def __stemmer(word):
    """
    .. versionadded:: 0.3.0

    Method for stemming a set of words.

    :param word: A word which should be stemmed.
    :type word: str.
    :returns: The porter stem of the input word.
    :rtype: str.
    """
    return _stemmer.stem(word)

def __is_stopword(word):
    """
    .. versionadded:: 0.3.0

    Returns true if the word appears in the nltk stopwords corpus.

    :param word: A query word which may or may not be a stopword.
    :type word: str.
    :returns: True or false, depending on whether the word appears in the nltk
              stopwords corpus.
    :rtype: bool
    """
    return (word in _stopwords)

def __remove_stopwords(list_of_words):
    """
    .. versionadded:: 0.3.0

    Remove stopwords from a list of words (in the form of strings).

    :param list_of_words: A list of words where each word is a string.
    :type list_of_words: str. list
    :returns: A list of strings where stopwords have been removed.
    :rtype: list

    .. code-block:: python

                    # This is 90% to show that it is possible,
                    # try not to this unless it's absolutely necessary.

                    from nltk import word_tokenize
                    from ffscraper.nlp.index import __remove_stopwords

                    sentence = 'i am writing fanfiction'
                    low = word_tokenize(sentence)
                    low_removed = __remove_stopwords(low)

                    print('Original:', low)
                    print('Stopwords Removed:', low_removed)

    .. code-block:: bash

                    Original: ['i', 'am', 'writing', 'fanfiction']
                    Stopwords Removed: ['writing', 'fanfiction']

    """
    return [word for word in list_of_words if not __is_stopword(word)]

def ngram(list_of_words, n=2):
    """
    Compute ngrams of a list of words. Returns bigrams by default.
    """
    pass

def invert():
    """
    .. versionadded:: 0.3.0

    Create an inverted index from the input corpus.
    """

if __name__ == '__main__':
    print('No main method in ffscraper.nlp.deconstruct')
    exit(1)
