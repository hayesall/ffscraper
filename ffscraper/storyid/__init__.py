
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

from __future__ import print_function

from ..utils import soupify
from tqdm import tqdm

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


def _number_of_pages(soup):
    """
    There are two center tags at the top and bottom of each page, containing
    information on how the fanfics are paginated.
    """

    # Initialize number_of_pages to 0.
    number_of_pages = 0

    for center_tag in soup.find_all('center'):
        for a_tag in center_tag.find_all('a'):
            if 'Last' in a_tag:
                # The last value in the list is the final page.
                number_of_pages = int(a_tag['href'].split('=')[-1])
                break

    # Return 0 or the updated number_of_pages.
    return number_of_pages


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

    soup = soupify(url, rate_limit=rate_limit)
    number_of_pages = _number_of_pages(soup)

    sids = []

    if number_of_pages:
        # If number_of_pages was assigned, then we may scrape the information
        for page in tqdm(range(1, number_of_pages+1)):
            sids += _get_sids(soupify(url + '?&p=' + str(page),
                                      rate_limit=rate_limit))
    else:
        # If number_of_pages is 0, get the first page.
        sids = _get_sids(soupify(url, rate_limit=rate_limit))

    return sids
