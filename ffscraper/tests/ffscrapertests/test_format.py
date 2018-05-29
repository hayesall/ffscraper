
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
import ffscraper as ffs

class formatTest(unittest.TestCase):

    def test_format_1(self):
        # Test using cytoscape format.

        expectation = {'cytoscape': 'harry friends ron'}
        reality = ffs.format('friends', 'harry', 'ron', cytoscape=True)
        self.assertEqual(expectation, reality)

    def test_format_2(self):
        # Test using predicate format.

        expectation = {'predicate': 'friends("harry","ron").'}
        reality = ffs.format('friends', 'harry', 'ron', predicate=True)
        self.assertEqual(expectation, reality)

    def test_format_3(self):
        # Test using both formats.

        expectation = {'cytoscape': 'harry friends ron',
                       'predicate': 'friends("harry","ron").'}
        reality = ffs.format('friends', 'harry', 'ron',
                             predicate=True, cytoscape=True)
        self.assertEqual(expectation, reality)

    def test_format_4(self):
        # This should raise an exception for providing too few arguments.

        with self.assertRaises(Exception):
            ffs.format('friends', 'harry', cytoscape=True)

    def test_format_5(self):
        # This should raise an exception for providing too many arguments.

        with self.assertRaises(Exception):
            ffs.format('friends', 'harry', 'ron', 'hermione', cytoscape=True)
