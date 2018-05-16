
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

# This set of tests is interested in ffscraper.fanfic.review
sys.path.append('./')
from ffscraper.fanfic import review

class ReviewsTest(unittest.TestCase):

    # ffscraper.fanfic.review

    def test_reviews_1(self):

        soup = bs("""<tbody><tr  >
                	<td  style='padding-top:10px;padding-bottom:10px'>
                    <span style='float:right'>
                    <a href='https://www.fanfiction.net/' style='color:#333333;
                    border-bottom:0px;' title='Reply to Review'></span>
                    <a href='/u/123/persona'>persona</a>
                    <small style='color:gray'>chapter 10 .
                    <span data-xutime='11111'>5/3</span>
                    </small><div style='margin-top:5px'>Most recent.</div>
                    </td></tr>
                    <tr  ><td  style='padding-top:10px;padding-bottom:10px'>
                    <span style='float:right'>
                    <a href='https://www.fanfiction.net/' style='color:#333333;
                    border-bottom:0px;' title='Reply to Review'></span>
                    <a href='/u/123/persona'>persona</a>
                    <small style='color:gray'>chapter 10 .
                    <span data-xutime='11110'>5/3</span>
                    </small><div style='margin-top:5px'>Same person.</div>
                    </td></tr>
                    <tr  ><td  style='padding-top:10px;padding-bottom:10px'>
                    <img class='round36' style='clear:left;float:left;
                    margin-right:3px;padding:2px;border:1px solid #ccc;
                    -moz-border-radius:2px;-webkit-border-radius:2px;'
                    src='/static/images/d_60_90.jpg' width=50 height=50> Guest
                    <small style='color:gray'>chapter 2 .
                    <span data-xutime='22222'>5/8/1985</span>
                    </small><div style='margin-top:5px'>Anonymous third.</div>
                    </td></tr></tbody>""", 'html.parser')

        reviews = review._reviews_in_table(soup)
        reality = [r for r in reviews]

        self.assertEqual(reality[0][0], '123')
        self.assertEqual(reality[0][1], '10')
        self.assertEqual(reality[0][2], '11111')
        self.assertEqual(reality[0][3], 'Most recent.')

        self.assertEqual(reality[1][0], '123')
        self.assertEqual(reality[1][1], '10')
        self.assertEqual(reality[1][2], '11110')
        self.assertEqual(reality[1][3], 'Same person.')

        self.assertEqual(reality[2][0], 'Guest')
        self.assertEqual(reality[2][1], '2')
        self.assertEqual(reality[2][2], '22222')
        self.assertEqual(reality[2][3], 'Anonymous third.')
