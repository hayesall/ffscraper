
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

from bs4 import BeautifulSoup as bs
import sys
import unittest

sys.path.append('./')

from ffscraper import storyid


class GetSidsTest(unittest.TestCase):

    def test_get_storyids_0(self):

        soup = bs("""""", 'html.parser')
        sids = storyid._get_sids(soup)
        self.assertEqual(sids, [])

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


class NumberOfPagesTest(unittest.TestCase):

    def test_get_number_of_pages_1(self):
        soup = bs("""""", 'html.parser')
        number_of_pages = storyid._number_of_pages(soup)
        self.assertEqual(0, number_of_pages)

    def test_get_number_of_pages_2(self):
        soup = bs("""<center style='margin-top:5px;'>5.2K | Page  <b>1</b>
        <a href='/book/Current-Story/?&srt=1&r=103&p=2'>2</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=3'>3</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=4'>4</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=11'>11</a>  ..
        <a href='/book/Current-Story/?&srt=1&r=103&p=301'>Last</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=2'>Next &#11;</a>
        </center>""", 'html.parser')
        number_of_pages = storyid._number_of_pages(soup)
        self.assertEqual(301, number_of_pages)

    def test_get_number_of_pages(self):
        soup = bs("""<center style='margin-top:5px;'>1.1K | Page  <b>1</b>
        <a href='/book/Current-Story/?&srt=1&r=103&p=2'>2</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=3'>3</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=4'>4</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=11'>11</a>  ..
        <a href='/book/Current-Story/?&srt=1&r=103&p=99'>Last</a>
        <a href='/book/Current-Story/?&srt=1&r=103&p=2'>Next &#11;</a>
        </center>""", 'html.parser')
        number_of_pages = storyid._number_of_pages(soup)
        self.assertEqual(99, number_of_pages)
