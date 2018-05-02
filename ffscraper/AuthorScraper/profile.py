
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

"""
A user's profile on FanFiction.Net may consist of some combination of a:
        1. uid (integer)
        2. username (string)
        3. beta profile (bool)
        4. My Stories
        5. Favorite Stories
        6. Favorite Authors
        7. Communities

Beta profile users additionally have additional properties:
    Beta Description:
        1. Beta Bio (general description as a beta reader)
        2. My Strengths (beta, writing, or reading strength)
        3. My Weaknesses (beta, writing, or reading weaknesses)
        4. Preferred (types of stories I prefer over others)
        5. Would Rather Not (I do not beta read for these stories)

    Beta Preferences:
        1. Language
        2. Content Rating (range of acceptable fiction ratings)
        3. Categories (categories in black are ones this beta has authored for)
        4. Genres (genres in black are ones this beta has authored for)

In practice, the 'My Stories' section is likely to be duplicate information
when FanfictionScraper.py already picks this information up.
"""

from __future__ import print_function

from bs4 import BeautifulSoup as bs

import requests
import time

def ScrapeProfile(uid, rate_limit=3):
    """
    Scrapes the data from a user's profile on FanFiction.Net

    @method ScrapeProfile
    @param  {uid}           uid         user id number for a particular user
    @param  {int}           rate_limit  time in seconds to enforce
    @return {dict}          prof        dictionary of profile information
    """

    # Rate Limit
    time.sleep(rate_limit)

    # Make a request to the site, make a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/u/' + uid)
    html = r.text
    soup = bs(html, 'html.parser')

    # "Favorite Stories" are stored in a z-list favstories
    favorite_stories = soup.find_all('div', {'class': 'z-list favstories'})

    print(favorite_stories[0])
    print(len(favorite_stories))


if __name__ == '__main__':
    # This behavior is for testing, will likely be deprecated or changed later.

    exit(0)
