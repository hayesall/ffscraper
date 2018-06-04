
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

from bs4 import BeautifulSoup as bs
import sys
import unittest

sys.path.append('./')

from ffscraper import storyid


class GetSidsTest(unittest.TestCase):

    def test_get_storyids_1(self):

        soup = bs("""<div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/111/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>""", 'html.parser')

        sids = storyid._get_sids(soup)
        self.assertEqual(sids, ['111'])

    def test_get_storyids_2(self):

        soup = bs("""<div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/111/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>
        <div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/114/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>""", 'html.parser')

        sids = storyid._get_sids(soup)
        self.assertEqual(sids, ['111', '114'])

    def test_get_storyids_3(self):

        soup = bs("""<div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/111/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>
        <div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/114/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>
        <div class='z-list zhover zpointer '
        style='min-height:77px;border-bottom:1px #cdcdcd solid;' >
        <a  class=stitle href="/s/2/1/This-Is-A-Title">
        This Is A Title</a>  by <a href="/u/4444/author-name">author name</a>
        </div>""", 'html.parser')

        sids = storyid._get_sids(soup)
        self.assertEqual(sids, ['111', '114', '2'])
