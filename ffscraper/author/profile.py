
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
from __future__ import division

from bs4 import BeautifulSoup as bs

import requests
import time

def _favorite_stories(soup):
    """
    .. versionadded:: 0.3.0

    Find the favorite stories and return them as a list.

    .. note:: Currently crossover fandoms are not split or taken into account
              closely. It may be useful to see how the crossover fandoms
              correlate with other stories that the user likes.

    :param soup: Soup containing a page from FanFiction.Net
    :type soup: bs4.BeautifulSoup class

    :returns: A list of story-ids liked by the user, and a dictionary mapping
              a fandom to all of the stories that are part of that fandom.
    :rtype: tuple
    """

    # "Favorite Stories" are stored in a z-list favstories.
    favorite_stories = soup.find_all('div', {'class': 'z-list favstories'})

    # Favorites as a list of tuples
    favs = []
    for story in favorite_stories:
        favs.append(tuple([_metadata_storyid(story), _metadata_fandom(story)]))

    # Favorites as an index mapping the fandom to the stories which are
    # part of the fandom.
    # e.g. favorites_inverted['Pride and Prejudice'] == ['124', '125', '127']
    favorites_inverted = {}
    for storyid, fandom in favs:
        if fandom in favorites_inverted:
            favorites_inverted[fandom].append(storyid)
        else:
            favorites_inverted[fandom] = [storyid]

    return favs, favorites_inverted

def _favorite_authors(soup):
    """
    .. versionadded:: 0.3.0

    Find the favorite authors for a user and return them as a list.

    :param soup: Soup containing a page from FanFiction.Net
    :type soup: bs4.BeautifulSoup class

    :returns: A list of user-ids corresponding to the authors liked by a user.
    :rtype: list

    Example:

    .. code-block:: python

                    import ffscraper as ffs

                    # Get an example user (details are changed here)
                    soup = ffs.utils.soupify('https://www.fanfiction.net/u/123')

                    # Get their favorite authors via this function.
                    fav_authors = ffs.author.profile._favorite_authors(soup)

                    # We'll print to see the results
                    print(fav_authors)

    .. code-block:: bash

                    ['124', '125', '126']
    """

    # Favorite Authors for a user is stored under a div with id='fa'
    authors_table = soup.find('div', {'id': 'fa'})
    if authors_table:
        author_links = authors_table.find_all('a')
        return [a['href'].split('/')[2] for a in author_links]
    else:
        return []

def _metadata_storyid(soup_tag):
    """
    .. versionadded:: 0.3.0

    Parses the story metadata for stories shown on a user's profile, returning
    the storyid.

    :param soup_tag: Tag containing <div class="z-list favstories" ...>
    :type soup_tag: bs4.element.Tag class
    """
    return soup_tag['data-storyid']

def _metadata_fandom(soup_tag):
    """
    .. versionadded:: 0.3.0

    Parses the story metadata for stories shown on a user's profile, returning
    the fandom.

    :param soup_tag: Tag containing <div class="z-list favstories" ...>
    :type soup_tag: bs4.element.Tag class
    """
    return soup_tag['data-category']

def _relative_likes(favorite_stories, inverted_favorites, fandom):
    """
    .. versionadded:: 0.3.0

    Returns how many stories a user likes in a fandom over all fandoms
    that they like.

    :param favorite_stories: List of story-ids liked by a user.
    :type favorite_stories: list.
    :param inverted_favorites: Dictionary mapping fandoms to the story-ids in
                               that fandom liked by a user.
    :type inverted_favorites: dict.
    :param fandom: String representing the fandom.
    :type fandom: str.

    :returns: Approximate calculation for how much a user likes a fandom.
    :rtype: float

    .. note:: This is far from a perfect calculation. This should really take
              a few more metrics into account, such as the number of stories
              a person has written for a particular fandom, the sentiment of
              the reviews they left over all stories they reviewed for a
              fandom, etc.
    """

    # Calculate roughly how much this person likes this fandom.
    number_of_favorites = len(favorite_stories)

    # If the user likes no fanfics
    if not number_of_favorites:
        return 0.0

    # If they like at least one story from the fandom, get the number.
    if inverted_favorites.get(fandom):
        favorites_for_fandom = len(inverted_favorites[fandom])
    else:
        return 0.0

    # If they like at least one fanfic and one from this fandom, return score.
    return favorites_for_fandom / number_of_favorites

def scraper(uid, rate_limit=3):
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

    >>> from ffscraper.author import profile
    >>> profile123 = profile.scraper('123')
    """

    # Rate Limit
    time.sleep(rate_limit)

    # Make a request to the site, make a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/u/' + uid)
    html = r.text
    soup = bs(html, 'html.parser')

    #soup.find_all('div', {'class': 'z-list favstories'})
    #Returns a tuple of (favorite_stories, inverted_favorites)
    return _favorite_stories(soup)
