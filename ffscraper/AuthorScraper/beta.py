
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

def ScrapeBeta(uid, rate_limit=3):
    """
    Scrapes the data from a user's beta profile on FanFiction.Net.

    Beta readers have profiles with some additional features beyond the normal
    profile, including:

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

    If a user is not a beta reader, their 'beta' page will list a warning
    which reads: '[username] is not a registered beta reader.'

    :param uid: User-id number for a person on FanFiction.Net.
    :type uid: str.
    :param rate_limit: Number of seconds to wait at the start of function call
                       in order to enforce scraper niceness.
    :type rate_limit: int.
    :returns: Currently returns nothing.

    .. note::
       This functionality may be more appropriate as a separate package for
       explicitly scraping beta profiles.
       https://www.fanfiction.net/betareaders/

    Example:

    >>> from ffscraper.AuthorScraper.beta import ScrapeBeta
    >>> ScrapeBeta('123')
    """

    # Rate Limit
    time.sleep(rate_limit)

    # Make a request to the site, make a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/beta/' + uid)
    html = r.text
    soup = bs(html, 'html.parser')
