
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
+----------------------+---------------------------------------------------+
|      **Name**        |                  **Description**                  |
+----------------------+---------------------------------------------------+
|       story.py       | A module for scraping a story from FanFiction.Net |
+----------------------+---------------------------------------------------+
"""

from __future__ import print_function
from __future__ import division

from . import review

from bs4 import BeautifulSoup as bs
import requests
import time

def _category_and_fandom(soup):
    """
    .. versionadded:: 0.3.0

    Returns the FanFiction category and fandom from the soup.

    * Category is one of nine possible categories from ``['Anime/Manga', 'Books',
      'Cartoons', 'Comics', 'Games', 'Misc', 'Movies', 'Plays/Musicals', 'TV']``
    * Fandom is the specific sub-category, whereas category may be
     ``Plays/Musicals``, the fandom could be ``RENT``, ``Wicked``, etc.

    :param soup: Soup containing a page from FanFiction.Net
    :type soup: bs4.BeautifulSoup class

    :returns: Tuple where the first item is the category and the second item is
              the fandom.

    .. code-block:: python

                    from ffscraper.fanfic.story import __category_and_fandom
                    from bs4 import BeautifulSoup as bs
                    import requests

                    r = requests.get('https://www.fanfiction.net/s/123')
                    html = r.text
                    soup = bs(html, 'html.parser')

                    print(_category_and_fandom(soup))

    .. code-block:: bash

                    ('Plays/Musicals', 'Wicked')
    """

    c_f = soup.find('div', {'id': 'pre_story_links'}).find_all('a', href=True)
    return c_f[0].text, c_f[1].text

def scraper(storyid, rate_limit=3):
    """
    .. versionadded:: 0.1.0

    Scrapes a story on FanFiction.Net

    :param storyid: Story-id number for a story on FanFiction.Net.
    :type uid: str.
    :param rate_limit: Number of seconds to wait at the start of function call
                       in order to enforce scraper niceness.
    :type rate_limit: int.
    :returns: Dictionary of data and metadata for the story.
    :rtype: dict.

    Example (*the output presented here has been altered*):

    .. code-block:: python

                    from ffscraper.fanfic import story

                    # story.scraper is a handy interface for all of these.
                    story123 = story.scraper('123')
                    print(story123)

    .. code-block:: bash

                    {'genre': 'Western', 'sid': '123', 'Reviewers':
                    ['12', '24'], 'rating': 'Rated: Fiction  K', 'aid': "241"}
    """

    # Rate limit
    time.sleep(rate_limit)

    # Make a request to the site, create a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/s/' + storyid)
    html = r.text
    soup = bs(html, 'html.parser')

    # Get the category and fandom information.
    category, fandom = _category_and_fandom(soup)

    # Get the metadata describing properties of the story.
    # This should contain the metadata line (e.g. rating, genre, words, etc.)
    metadata_html = soup.find('span', {'class': 'xgray xcontrast_txt'})
    metadata = metadata_html.text.replace('Sci-Fi', 'SciFi')
    metadata = [s.strip() for s in metadata.split('-')]

    # Title from <b class='xcontrast_txt'>...</b>
    title = soup.find('b', {'class': 'xcontrast_txt'}).text

    # Abstract and story are identified by <div class='xcontrast_txt'>...</div>
    abstract_and_story = soup.find_all('div', {'class': 'xcontrast_txt'})
    abstract = abstract_and_story[0].text
    story_text = abstract_and_story[1].text

    # 'Publication' and 'last updated' are the two timestamps which are available.
    # If only one timestamp is listed, the story's update and publication time
    # should be the same.
    timestamps = metadata_html.find_all(attrs={'data-xutime': True})
    if len(timestamps) == 1:
        when_updated = timestamps[0]['data-xutime']
        when_published = when_updated
    else:
        when_updated = timestamps[0]['data-xutime']
        when_published = timestamps[1]['data-xutime']

    # There are several links on the page, the 2nd is a link to the author's
    # page. Get the second link href tag (which will look something like '/u/1838183/thisname')
    authorid = soup.find_all('a', {'class': 'xcontrast_txt'})[2].get('href').split('/')[2]

    #print(metadata_html.find_all(attrs={'data-xutime': True}))
    story = {
        'sid': storyid,
        'aid': authorid,
        #'category': category,
        #'fandom': fandom,
        #'title': title,
        #'published': when_published,
        #'updated': when_updated,
        'rating': metadata[0],
        'genre': metadata[2]
        #'metadata': metadata,
        #'abstract': abstract,
        #'story_text': story_text
    }

    for m in metadata:
        if 'Reviews' in m:

            num_of_reviews = int(m.split()[1])
            users = review.ReviewIDScraper(storyid, num_of_reviews)
            story['Reviewers'] = users

    #print(metadata)

    #print(soup.prettify())
    return story
