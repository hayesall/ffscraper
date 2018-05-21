
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

import sys
import unittest

sys.path.append('./')

from ffscraper import utils

class PredicateLogicBuilderTest(unittest.TestCase):

    def test_PredicateLogicBuilder_1(self):

        expectation = 'liked("123","1335").'
        reality = utils.PredicateLogicBuilder('liked', '123', '1335')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_2(self):

        expectation = 'author("a","b").'
        reality = utils.PredicateLogicBuilder('author', 'a', 'b')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_3(self):

        expectation = 'author("a_b","b_c").'
        reality = utils.PredicateLogicBuilder('author', 'a_b', 'b_c')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_4(self):

        expectation = 'author("ab","bc").'
        reality = utils.PredicateLogicBuilder('author', 'a  b', 'b  c')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_5(self):

        expectation = 'author("a_b","b_c").'
        reality = utils.PredicateLogicBuilder('author', 'a _ b', 'b _ c')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_6(self):

        expectation = ' author ("a","b").'
        reality = utils.PredicateLogicBuilder(' author ', 'a', 'b')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_7(self):

        expectation = 'words("38,183").'
        reality = utils.PredicateLogicBuilder('words', '38,183', '')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_8(self):

        expectation = 'words("11aabb").'
        reality = utils.PredicateLogicBuilder('words', ' 11 aa bb ', '')
        self.assertEqual(expectation, reality)

    def test_PredicateLogicBuilder_9(self):

        expectation = ' words ("88").'
        reality = utils.PredicateLogicBuilder(' words ', '    88   ', '')
        self.assertEqual(expectation, reality)
