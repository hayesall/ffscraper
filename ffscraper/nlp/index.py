
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

   ``ffscraper.nlp.index.normalize`` has a ``language`` parameter for
   specifying the input language (based on ``nltk.stopwords`` corpora), but
   these have not been thoroughly tested.

**Basic example to highlight features:**

.. code-block:: python

                import ffscraper as ffs

                basic_example = '''This is a short example. I want to build a
                search engine for fanfiction.
                '''

                # Normalize our example with some NLP techniques, first by
                # splitting our input into sentences, then splitting the
                # sentences into lowercase words with punctuation removed.
                sentences = ffs.nlp.index.normalize(basic_example)

                print('Sentences after ffs.nlp.index.normalize:')
                for sentence in sentences:
                    print(sentence)

.. code-block:: bash

                ['short', 'exampl', '']
                ['want', 'build', 'search', 'engin', 'fanfict', '']

**Example with a larger input corpus:**

.. code-block:: python

                import ffscraper as ffs

                declaration = '''When in the course of human events it
                becomes necessary for one people to dissolve the political
                bands which have connected them with another and to assume
                among the powers of the earth, the separate and equal station
                to which the Laws of Nature and of Nature's God entitle them,
                a decent respect to the opinions of mankind requires that they
                should declare the causes which impel them to the separation.

                We hold these truths to be self-evident, that all men are
                created equal, that they are endowed by their Creator with
                certain unalienable Rights, that among these are Life,
                Liberty and the pursuit of Happiness. That to secure these
                rights, Governments are instituted among Men, deriving their
                justpowers from the consent of the governed, That whenever
                any Form of Government becomes destructive of these ends,
                it is the Right of the People to alter or to abolish it, and
                to institute new Government, laying its foundations on such
                principles and organizing its powers in such form, as to them
                shall seem most likely to effect their Safety and Happiness.
                '''

                # Normalize our input by splitting into sentences, and further
                # splitting each sentence into lowercase words with stopwords
                # and punctuation removed.
                sentences = ffs.nlp.index.normalize(declaration)

                for sentence in sentences:
                    print(sentence)

.. code-block:: bash

                ['cours', 'human', 'event', 'becom', 'necessari', 'one',
                'peopl', 'dissolv', 'polit', 'band', 'connect', 'anoth',
                'assum', 'among', 'power', 'earth', '', 'separ', 'equal',
                'station', 'law', 'natur', 'natur', 'god', 'entitl', '',
                'decent', 'respect', 'opinion', 'mankind', 'requir', 'declar',
                'caus', 'impel', 'separ', '']
                ...[snipped]
"""

from __future__ import print_function
from __future__ import unicode_literals

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *

import string

_punctuation = string.punctuation
_stemmer = PorterStemmer()
_stopwords = stopwords.words('english')

def __stem(word):
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

def __remove_stopwords(list_of_words, language='english'):
    """
    .. versionadded:: 0.3.0

    Remove stopwords from a list of words (in the form of strings).

    :param list_of_words: A list of words where each word is a string.
    :type list_of_words: str. list
    :param language: A string representing the language the list of words
                     is in [Default: 'english'].
    :type language: str.
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
    if language is not 'english':
        return [word for word in list_of_words if word not in stopwords.words(language)]
    else:
        return [word for word in list_of_words if not __is_stopword(word)]

def ngram(list_of_words, n=2):
    """
    Compute ngrams of a list of words. Returns bigrams by default.
    """
    pass

def __count_and_log(input):
    pass

def invert():
    pass

def normalize(string, language='english'):
    """
    .. versionadded:: 0.3.0

    Create an inverted index from the input.

    :param string: A string, potentially with punctuation and newlines.
    :type string: str.
    :param language: Language of the input string.
    :type language: str.

    :returns: A generator. Each item corresponds to a sentence in the string,
              each list consists of strings of lowercase words which have been
              stopped and stemmed.
    :rtype: generator

    Order of operations:

    1. Use ``nltk.sent_tokenize`` to split the input string into a list of
       sentences.
    2. Use ``nltk.word_tokenize`` on each sentence.
    3. Convert words to lowercase and remove punctuation.
    4. Remove stopwords from each of the sentences (dependent on the language).
    """

    # Split the input string into sentences with nltk.sent_tokenize
    sentences = sent_tokenize(string)

    for sentence in sentences:

        # 1. Tokenize the words.
        words = word_tokenize(sentence)

        # 2. Convert the words to lowercase and remove punctuation.
        tokens = [word.lower().strip(_punctuation) for word in words]

        # 3. Remove stopwords from the list of tokens.
        stopped_tokens = __remove_stopwords(tokens, language=language)

        # 4. Stem the stopped_tokens
        stemmed_stopped_tokens = [__stem(word) for word in stopped_tokens]

        # Yield results
        yield stemmed_stopped_tokens
