
# -*- coding: utf-8 -*-

#   Copyright (c) 2018-2019 Alexander L. Hayes (@hayesall)
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
from ffscraper.format import cytoscape

class cytoscapeFormatTest(unittest.TestCase):

    def test_cytoscapeFormat_1(self):

        expectation = '123 liked 1335'
        reality = cytoscape.cytoscapeFormat('liked', '123', '1335')
        self.assertEqual(expectation, reality)

    def test_cytoscapeFormat_2(self):

        expectation = 'a author b'
        reality = cytoscape.cytoscapeFormat('author', 'a', 'b')
        self.assertEqual(expectation, reality)

    def test_cytoscapeFormat_3(self):

        expectation = 'a_b author b_c'
        reality = cytoscape.cytoscapeFormat('author', 'a_b', 'b_c')
        self.assertEqual(expectation, reality)

    def test_cytoscapeFormat_4(self):

        expectation = 'ab author bc'
        reality = cytoscape.cytoscapeFormat('author', 'a  b', 'b  c')
        self.assertEqual(expectation, reality)

    def test_cytoscapeFormat_5(self):

        expectation = 'a_b author b_c'
        reality = cytoscape.cytoscapeFormat('author', 'a _ b', 'b _ c')
        self.assertEqual(expectation, reality)

    def test_cytoscapeFormat_6(self):

        expectation = 'a author b'
        reality = cytoscape.cytoscapeFormat(' author ', 'a', 'b')
        self.assertEqual(expectation, reality)
