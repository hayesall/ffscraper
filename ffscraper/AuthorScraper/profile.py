
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

import requests
import time

def ScrapeProfile(uid, rate_limit=3):
    """
    Scrapes the data from a user's profile on FanFiction.Net.

    A user's profile may consist of some combination of a:
      1. uid
      2. username
      3. beta profile
      4. My Stories
      5. Favorite Stories
      6. Favorite Authors
      7. Communities

    In practice, the 'My Stories' section may duplicate information when
    FanfictionScraper.py already picks this up elsewhere. Nevertheless,
    this information may be of greater interest in certain contexts,
    such as explicitly looking at all of the stories that someone authored.

    :param uid: User-id number for a person on FanFiction.Net.
    :type uid: str.
    :param rate_limit: Number of seconds to wait at the start of function call
                       in order to enforce scraper niceness.
    :type rate_limit: int.
    :returns: Currently returns nothing.

    >>> from ffscraper.AuthorScraper.profile import ScrapeProfile
    >>> ScrapeProfile('123')
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
