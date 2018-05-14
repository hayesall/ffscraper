
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

class StoryTest(unittest.TestCase):

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
