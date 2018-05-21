
# -*- coding: utf-8 -*-

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

from __future__ import print_function

from collections import Counter

import sys
import unittest

sys.path.append('./')

from ffscraper.nlp import index

class IndexTest(unittest.TestCase):

    def test_normalize_1(self):
        # Basic test with uppercase letters and punctuation.

        sentence_generator = index.normalize(u'Hello World!')
        sentences = [sentence for sentence in sentence_generator]
        self.assertEqual(sentences, [['hello', 'world', '']])

    def test_normalize_2(self):
        # Test with a variety of characters and punctuation over several lines.

        sentence_generator = index.normalize(u'''In 19th-Century Russia we write
        letters we write letters, we put down in writing what is happening in
        our minds. Once it's on the paper we feel better we feel better, it's
        like some kind of clarity when the letter's done and signed.
        ''')

        sentences = [sentence for sentence in sentence_generator]
        expected = [[u'19th-centuri', 'russia', 'write', u'letter', 'write',
        u'letter', '', 'put', u'write', u'happen', u'mind', ''],
        ['paper', 'feel', 'better', 'feel', 'better', '', 'like', 'kind',
        u'clariti', 'letter', 'done', u'sign', '']]

        self.assertEqual(sentences, expected)

    def test_normalize_3(self):
        # Test with possibly unconventional input: an empty string.

        sentence_generator = index.normalize('', language='english')
        sentences = [sentence for sentence in sentence_generator]
        expected = []

        self.assertEqual(sentences, expected)

    def test_normalize_4(self):
        # Test with possibly unconventional input: an empty string in French.

        sentence_generator = index.normalize('', language='french')
        sentences = [sentence for sentence in sentence_generator]
        expected = []

        self.assertEqual(sentences, expected)

    def test_normalize_5(self):
        # Test with French instead of English.

        sentence_generator = index.normalize(u'''Alouette, gentille alouette,
        Alouette, je te plumerai. Je te plumerai la tête.''', language='french')

        sentences = [sentence for sentence in sentence_generator]
        expected = [[u'alouett', u'', u'gentil', u'alouett', u'', u'alouett',
        u'', u'plumerai', u''], [u'plumerai', u'tête', u'']]

        self.assertEqual(sentences, expected)

class WordcountTest(unittest.TestCase):

    def test_wordcount_1(self):
        # 1. The example supplied in the documentation.

        doc = index.normalize(u'''O Captain! my Captain! our fearful trip
                is done, The ship has weather'd every rack, the prize we
                sought is won, The port is near, the bells I hear, the
                people all exulting, While follow eyes the steady keel,
                the vessel grim and daring; But O heart! heart! heart!
                O the bleeding drops of red, Where on the deck my Captain
                lies, Fallen cold and dead.''', language='english')

        expected = Counter({'captain': 3, 'heart': 3, 'fear': 1, 'trip': 1,
                'done': 1, 'ship': 1, 'weather': 1, 'everi': 1, 'rack': 1,
                'prize': 1, 'sought': 1, 'port': 1, 'near': 1, 'bell': 1,
                'hear': 1, 'peopl': 1, 'exult': 1, 'follow': 1, 'eye': 1,
                'steadi': 1, 'keel': 1, 'vessel': 1, 'grim': 1, 'dare': 1,
                'bleed': 1, 'drop': 1, 'red': 1, 'deck': 1, 'lie': 1,
                'fallen': 1, 'cold': 1, 'dead': 1})

        self.assertEqual(index.wordcount(doc), expected)

    def test_wordcount_2(self):
        # 2. A short example where we can easily count the words.

        doc = index.normalize(u'Hello hello hello world goodbye')
        expected = Counter({'hello': 3, 'world': 1, 'goodby': 1})
        self.assertEqual(index.wordcount(doc), expected)

    def test_wordcount_3(self):
        # 3. Possibly strange input: where we normalize an empty string.

        doc = index.normalize('')
        expected = Counter({})
        self.assertEqual(index.wordcount(doc), expected)

    def test_wordcount_4(self):
        # 4. Examples so far have used the index.normalize function, this
        #    test uses lists of lists of strings.

        doc = [['a', 'b', 'c'], ['a', 'b', 'd'], ['a', 'a', 'a']]
        expected = Counter({'a': 5, 'b': 2, 'c': 1, 'd': 1})
        self.assertEqual(index.wordcount(doc), expected)
