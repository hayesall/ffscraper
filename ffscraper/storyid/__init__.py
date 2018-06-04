
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
Scrape the story-ids based on an input url.
"""

from ..utils import soupify


def _get_sids(soup):
    """
    Find all story links in the soup.

    :param soup: Soup containing a page from FanFiction.Net
    :type soup: bs4.BeautifulSoup class

    :returns: A list of story-ids, up to 25.
    :rtype: list of strings.
    """

    stories = soup.find_all('a', {'class': 'stitle'}, href=True)

    # Each page may contain up to 25 sids, append each of them to a list.
    sids = []

    for h in stories:
        # Each href is of the form: /s/111/1/Title-Like-This
        sids.append(h['href'].split('/')[2])

    return sids


def scrape(url, rate_limit=3):
    """
    Scrape all story-ids found on a particular page.

    :param url: Url for a page on FanFiction.Net
    :type url: str.
    :param rate_limit: Number of seconds to wait at the start of function call
                       in order to enforce scraper niceness.
    :type rate_limit: int.

    :returns: A list of story-ids, up to 25.
    :rtype: list of strings.
    """

    return _get_sids(soupify(url, rate_limit=rate_limit))
