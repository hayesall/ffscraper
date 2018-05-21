
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

from bs4 import BeautifulSoup as bs
import sys
import unittest

# This set of tests is interested in ffscraper.fanfic.story
sys.path.append('./')
from ffscraper.fanfic import story

class CategoryAndFandomTest(unittest.TestCase):

    def test_category_and_fandom_1(self):
        # 1: Check Plays/Musicals category and fandom.

        soup = bs("""<div style='margin-bottom: 10px' class='lc-wrapper'
        id=pre_story_links><span class=lc-left><a class=xcontrast_txt
        href='/play/'>Plays/Musicals</a>
        <span class='xcontrast_txt icon-chevron-right xicon-section-arrow'>
        </span><a class=xcontrast_txt href="/play/RENT/">RENT</a></span></div>
        """, 'html.parser')

        category, fandom = story._category_and_fandom(soup)

        self.assertEqual(category, 'Plays/Musicals')
        self.assertEqual(fandom, 'RENT')

    def test_category_and_fandom_2(self):
        # 2. Check an Anime/Manga category and fandom.

        soup = bs("""<div style='margin-bottom: 10px' class='lc-wrapper'
        id=pre_story_links><span class=lc-left>
        <a class=xcontrast_txt href='/anime/'>Anime/Manga</a>
        <span class='xcontrast_txt icon-chevron-right xicon-section-arrow'>
        </span><a class=xcontrast_txt href="/anime/Inuyasha/">Inuyasha</a>
        </span></div>""", 'html.parser')

        category, fandom = story._category_and_fandom(soup)

        self.assertEqual(category, 'Anime/Manga')
        self.assertEqual(fandom, 'Inuyasha')

    def test_category_and_fandom_3(self):
        # 3. Check an Anime/Manga fandom with less-frequent characters.
        #    Encoding issues may arise in Python 2.7 with ascii vs. unicode.
        #    In these cases it should be noted that unicode is not default,
        #    so u'' is specified for the strings.

        soup = bs(u"""<div style='margin-bottom: 10px' class='lc-wrapper'
        id=pre_story_links><span class=lc-left>
        <a class=xcontrast_txt href='/anime/'>Anime/Manga</a>
        <span class='xcontrast_txt icon-chevron-right xicon-section-arrow'>
        </span><a class=xcontrast_txt href="/anime/Attack-on-Titan-%E9%80%B2%E6%92%83%E3%81%AE%E5%B7%A8%E4%BA%BA/">Attack on Titan/進撃の巨人</a>
        </span></div>""", 'html.parser')

        category, fandom = story._category_and_fandom(soup)

        self.assertEqual(category, 'Anime/Manga')
        self.assertEqual(fandom, u'Attack on Titan/進撃の巨人')

        self.assertTrue(True)

class NotEmptyFanficTest(unittest.TestCase):

    def test_empty_fanfic_1(self):
        # 1. Test when the fanfic is empty (a.k.a. contains the error code)
        soup = bs(u"""<span class="gui_warning">Story Not Found
                    <hr noshade="" size="1"/>Unable to locate story.
                    Code 1.</span>""", 'html.parser')
        self.assertFalse(story._not_empty_fanfic(soup))

    def test_empty_fanfic_2(self):
        # 2. Test when the fanfic is not empty.
        soup = bs('', 'html.parser')
        self.assertTrue(story._not_empty_fanfic(soup))

    def test_empty_fanfic_3(self):
        # 3. Test when the fanfic is not empty, but contains something...
        soup = bs(u"""<div style='margin-bottom: 10px' class='lc-wrapper'
        id=pre_story_links><span class=lc-left>
        <a class=xcontrast_txt href='/anime/'>Anime/Manga</a>
        <span class='xcontrast_txt icon-chevron-right xicon-section-arrow'>
        </span><a class=xcontrast_txt href="/anime/Attack-on-Titan-%E9%80%B2%E6%92%83%E3%81%AE%E5%B7%A8%E4%BA%BA/">Attack on Titan/進撃の巨人</a>
        </span></div>""", 'html.parser')
        self.assertTrue(story._not_empty_fanfic(soup))

class TitleTest(unittest.TestCase):

    def test_title_1(self):
        # 1. Test generic input.

        soup = bs("<b class='xcontrast_txt'>Hello World</b>", 'html.parser')
        self.assertEqual(story._title(soup), 'Hello World')

    def test_title_2(self):
        # 2. Test with unicode characters.
        soup = bs(u"<b class='xcontrast_txt'>Attack on Titan/進撃の巨人</b>",
        'html.parser')
        self.assertEqual(story._title(soup), u'Attack on Titan/進撃の巨人')

    def test_title_3(self):
        # 3. Test with potentially strange input: no title.
        soup = bs("<b class='xcontrast_txt'></b>", 'html.parser')
        self.assertEqual(story._title(soup), '')

class TimestampsTest(unittest.TestCase):

    def test_timestamp_1(self):
        # 1. Test case where Published and Updated are the same.

        soup = bs(u"""<span class='xgray xcontrast_txt'>Rated:
        <a class='xcontrast_txt' href='https://www.fictionratings.com/'
        target='rating'>Fiction  K+</a> - French  - Words: 2,100 - Reviews:
        <a href='/r/15/'>103</a> - Favs: 3 - Follows: 5 - Published:
        <span data-xutime='1123840800'>8/12/2005</span> - id: 15 </span>""",
        'html.parser')

        published, updated = story._timestamps(soup)
        self.assertEqual(published, '1123840800')
        self.assertEqual(updated, '1123840800')

    def test_timestamp_2(self):
        # 2. Test case where Published and Updated are different.

        soup = bs(u"""<span class='xgray xcontrast_txt'>Rated:
        <a class='xcontrast_txt' href='https://www.fictionratings.com/'
        target='rating'>Fiction  T</a> - English - Chapters: 6   -
        Words: 6,198 - Reviews: <a href='/r/200/'>19</a> -
        Updated: <span data-xutime='183818181'>5/5/2000</span> -
        Published: <span data-xutime='12392811'>5/5/1999</span> -
        id: 200 </span>""", 'html.parser')

        published, updated = story._timestamps(soup)
        self.assertEqual(published, '12392811')
        self.assertEqual(updated, '183818181')
