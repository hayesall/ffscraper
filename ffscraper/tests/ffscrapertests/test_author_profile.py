
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

# This set of tests is interested in ffscraper.fanfic.author
sys.path.append('./')
from ffscraper.author import profile

class FavoriteStoriesTest(unittest.TestCase):

    # ffscraper.fanfic.author._favorite_stories

    def test_favorites_stories_1(self):
        # Three stories from same fandom.
        soup = bs("""<div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="120"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="121"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="122"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)
        self.assertEqual(fav_list, [('120', 'Pride and Prejudice'),
                                    ('121', 'Pride and Prejudice'),
                                    ('122', 'Pride and Prejudice')])
        self.assertEqual(fav_inverted, {'Pride and Prejudice':
                                        ['120', '121', '122']})

    def test_favorites_stories_2(self):
        # One story.
        soup = bs("""<div class='z-list favstories'
                data-category="Twilight"  data-storyid="500"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)
        self.assertEqual(fav_list, [('500', 'Twilight')])
        self.assertEqual(fav_inverted, {'Twilight': ['500']})

    def test_favorites_stories_3(self):
        # No favorites
        soup = bs("""""", 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)
        self.assertEqual(fav_list, [])
        self.assertEqual(fav_inverted, {})

    def test_favorites_stories_4(self):
        # Mix of fandom.
        soup = bs("""<div class='z-list favstories'
                data-category="Twilight"  data-storyid="500"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="121"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)
        self.assertEqual(fav_list, [('500', 'Twilight'),
                                    ('121', 'Pride and Prejudice')])
        self.assertEqual(fav_inverted, {'Twilight': ['500'],
                                        'Pride and Prejudice': ['121']})

class TestRelativeLikes(unittest.TestCase):

    # ffscraper.fanfic.author._relative_likes

    def test_relative_likes_1(self):
        # 1. Test using profile._favorite_stories to create the list and dict.
        soup = bs("""<div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="120"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="121"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="122"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)

        relative_likes = profile._relative_likes(fav_list, fav_inverted,
                                                 'Pride and Prejudice')
        self.assertEqual(1.0, relative_likes)

    def test_relative_likes_2(self):
        # 2. Test using profile._favorite_stories with no likes.
        soup = bs('', 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)
        relative_likes = profile._relative_likes(fav_list, fav_inverted,
                                                 'Pride and Prejudice')
        self.assertEqual(0.0, relative_likes)

    def test_relative_likes_3(self):
        # 3. Test using profile._favorite_stories with mix of fandom.
        soup = bs("""<div class='z-list favstories'
                data-category="Twilight"  data-storyid="500"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="121"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)

        relative_likes = profile._relative_likes(fav_list, fav_inverted,
                                                 'Pride and Prejudice')
        self.assertEqual(0.5, relative_likes)

    def test_relative_likes_4(self):
        # 4. Same test as test_relative_likes_3, but with 'Twilight'
        soup = bs("""<div class='z-list favstories'
                data-category="Twilight"  data-storyid="500"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="121"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)

        relative_likes = profile._relative_likes(fav_list, fav_inverted,
                                                 'Twilight')
        self.assertEqual(0.5, relative_likes)

    def test_relative_likes_5(self):
        # 5. Test when querying for a fandom that the user has not liked.
        soup = bs("""<div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="120"</div>

                <div class='z-list favstories'
                data-category="Pride and Prejudice"  data-storyid="122"</div>
                """, 'html.parser')

        fav_list, fav_inverted = profile._favorite_stories(soup)

        relative_likes = profile._relative_likes(fav_list, fav_inverted,
                                                 'Twilight')
        self.assertEqual(0.0, relative_likes)
