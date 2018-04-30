
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
## FanfictionScraper.py

A script for scraping a single fanfic from FanFiction.Net
"""

from __future__ import print_function
from __future__ import division

from . import review

from bs4 import BeautifulSoup as bs
import requests
import time

def FanfictionScraper(storyid, rate_limit=3):
    """
    Scrapes data from a story on FanFiction.Net

    @method FanfictionScraper
    @param  {str}               storyid         the id for a particular story
    @param  {int}               rate_limit      rate limit (in seconds)
    @return {dict}              story           dictionary of data and metadata
    """

    # Rate limit
    time.sleep(rate_limit)

    # Make a request to the site, create a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/s/' + storyid)
    html = r.text
    soup = bs(html, 'html.parser')

    # Get the category and fandom information.
    c_f = soup.find('div', {'id': 'pre_story_links'}).find_all('a', href=True)
    category = c_f[0].text
    fandom = c_f[1].text

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

if __name__ == '__main__':

    raise(Exception('No main class in FanfictionScraper.py'))
    exit(1)
