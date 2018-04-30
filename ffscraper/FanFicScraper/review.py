
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

def ReviewIDScraper(storyid, reviews_num, rate_limit=3):
    """
    Scrapes the reviews for a certain story, but only returns the user ids.

    ### Deprecation Warning;
    This is most likely a short-term hack for this specific function.
    As ReviewScraper.py is finalized this will likely be absorbed into
    the ReviewScraper function or reimagined as a function in a class.

    @method ReviewIDScraper

    @return {list}      list of user ids with duplicates removed.
    """
    number_of_pages = (reviews_num // 15) + 1

    user_id_list = []

    for p in range(number_of_pages):

        # Rate limit
        time.sleep(rate_limit)

        r = requests.get('https://www.fanfiction.net/r/' + storyid + '/0/' + str(p+1) + '/')
        html = r.text
        soup = bs(html, 'html.parser')

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


def ReviewScraper(storyid, reviews_num, rate_limit=3):
    """
    Scrapes the reviews for a certain story.

    @method ReviewScraper
    @param  {str}               storyid         The id for a particular story.
    @param  {int}               reviews_num     The number of reviews in metadata
    @param  {int}               rate_limit      rate limit (in seconds)
    @return {}

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

    for p in range(number_of_pages):

        # Rate limit
        time.sleep(rate_limit)

        r = requests.get('https://www.fanfiction.net/r/' + storyid + '/0/' + str(p+1) + '/')
        html = r.text
        soup = bs(html, 'html.parser')

        # Get the tbody, which is where the review table is stored
        t = soup.find('tbody')

        # Loop over the table entries (td)
        for review in t.find_all('td'):

            # Reviews link to the profile of the user who reviewed it.
            for link in review.find_all('a', href=True):

                if '/u/' in str(link):
                    # This is a way to get the user id.
                    print(str(link).split('"')[1].split('/')[2])

            '''
            print(review.text)
            #exit()
            time.sleep(0.5)
            '''

        #exit()

        #print(p+1)

if __name__ == '__main__':

    raise(Exception('No main class in ReviewScraper.py'))
    exit(1)
