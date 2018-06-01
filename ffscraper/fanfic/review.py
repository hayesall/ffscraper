
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
|       review.py      | A module for scraping reviews from FanFiction.Net |
+----------------------+---------------------------------------------------+
"""

from __future__ import print_function
from __future__ import division

from bs4 import BeautifulSoup as bs

from ..utils import soupify

import requests
import time


def ReviewIDScraper(storyid, reviews_num, rate_limit=3):
    """
    .. deprecated:: 0.3.0

       Use :func:`scraper` instead.

    """
    pass
    """
    number_of_pages = (reviews_num // 15) + 1

    user_id_list = []

    for p in range(number_of_pages):

        # Rate limit
        time.sleep(rate_limit)

        soup = soupify('https://www.fanfiction.net/r/' + storyid +
                       '/0/' + str(p+1) + '/')

        # Get the tbody, which is where the review table is stored
        t = soup.find('tbody')

        # Loop over the table entries (td)
        for review in t.find_all('td'):

            # Reviews link to the profile of the user who reviewed it.
            for link in review.find_all('a', href=True):

                if '/u/' in str(link):
                    # This is a way to get the user id.
                    user_id_list.append(str(link).split('"')[1].split('/')[2])

    return list(set(user_id_list))
    """


def _review_chapter_and_timestamp(soup_tag):
    """
    .. versionadded:: 0.3.0

    Returns the chapter that a review corresponds to and the timestamp
    when the review was left.

    :returns: Tuple where the first item is the chapter being reviewed and
              the second item is the timestamp when the review was left.
    :rtype: tuple
    """

    # Chapter and timestamp are listed under a <small> tag.
    small_tag = soup_tag.find('small')

    # Remove the space from the end and 'chapter ' from beginning.
    chapter = small_tag.text.split('.')[0][:-1].strip('chapter ')
    # Timestamp is the second item in the small_tag
    time_stamp = small_tag.find(attrs={'data-xutime': True})['data-xutime']

    return chapter, time_stamp


def _review_text(soup_tag):
    """
    .. versionadded:: 0.3.0

    Returns the text in a review entry.
    """
    return soup_tag.find('div', style='margin-top:5px').text


def _review_user(soup_tag):
    """
    .. versionadded:: 0.3.0.

    Returns the user id of the user who left the review. If the review was
    submitted anonymously, there will not be a link to the user who left it.
    """

    # Several links are listed under each review, only some are of interest.
    links = soup_tag.find_all('a', href=True)

    for link in links:
        if '/u/' in str(link):
            # Return the user id:
            return str(link).split('"')[1].split('/')[2]

    # If we did not reach a return during the for loop, this is a Guest review.
    # Guests are usually named "Guest" but occasionally they have a name
    # associated with them still.
    return 'Guest'


def _reviews_in_table(soup):
    """
    .. versionadded:: 0.3.0

    Finds all reviews in the review table in the soup.

    :param soup: Soup containing a page from FanFiction.Net
    :type soup: bs4.BeautifulSoup class

    :returns: A generator for 4-tuples, where items in the tuple correspond
              to (reviewer, chapter, timestamp, review_text).

              1. reviewer: Who left the review (user-id or 'Guest')
              2. chapter: Chapter the review was left for.
              3. timestamp: When the review was left.
              4. review_text: Content of the review.
    """

    # Get the tbody, which is where the review table is stored.
    tbody = soup.find('tbody')

    # Loop over the table entries (td)
    for review in tbody.find_all('td'):

        # Get the timestamp and the chapter being reviewed
        chapter, timestamp = _review_chapter_and_timestamp(review)

        # Get the user who left the review (or anonymous).
        reviewer = _review_user(review)

        # Get the review text associated with the current review.
        review_text = _review_text(review)

        yield (reviewer, chapter, timestamp, review_text)


def scraper(storyid, reviews_num, rate_limit=3):
    """
    Scrapes the reviews for a certain story.

    :param storyid: Story-id number for a story on FanFiction.Net.
    :type storyid: str.
    :param reviews_num: Number of reviews according to the metadata.
    :type reviews_num: int.
    :param rate_limit: Number of seconds to wait at the start of function call
                       in order to enforce scraper niceness.
    :type rate_limit: int.

    :returns: A list of review tuples, where each tuple corresponds to:
              (reviewer, chapter, timestamp, review_text).
    :rtype: list of strings.

    1. reviewer: Who left the review (user-id or 'Guest')
    2. chapter: Chapter the review was left for.
    3. timestamp: When the review was left.
    4. review_text: Content of the review.

    Discussion:
        * Reviews on FanFiction.Net may either be anonymous or tied to the user
          who left the review.
        * Reviews for a story are located at address:
          https://www.fanfiction.net/r/[sid]/0/1/
        * /0/ represents all reviews for a story, /1/ is a page, and there are
          up to 15 reviews per page.
        * Incrementing the 0 gives the reviews for a particular chapter.

    Page Layout:
        * Reviews are stored in an html table of up to 15 elements.
        * A review may be thought of as a 4-tuple:
            (userid, chapter_reviewed, date, review_text)
    """

    # There may be up to 15 reviews on a single page, therefore the number of
    # pages the reviews  are stored on is equal to the following:
    number_of_pages = (reviews_num // 15) + 1

    # Returns a list of tuples (based on the contents of _reviews_in_table)
    list_of_review_tuples = []

    for p in range(number_of_pages):

        # Rate limit
        time.sleep(rate_limit)

        soup = soupify('https://www.fanfiction.net/r/' + storyid +
                       '/0/' + str(p+1) + '/')

        for review in _reviews_in_table(soup):
            list_of_review_tuples.append(review)

    return list_of_review_tuples
