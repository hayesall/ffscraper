
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
__main__.py currently has three "Phases", this is an in-progress attempt at
consolidating them into functions.
"""

from __future__ import print_function

# Python Standard Library Modules
from heapq import heappush
from heapq import heappop

# Non-Standard Library Modules
from textblob import TextBlob
from tqdm import tqdm

# Relative imports from ffscraper
from .fanfic import story
from .fanfic import review
from .author import profile
from . import utils

# Phase I: Scraping stories

def phase1(sids, scrape_reviews=True):
    """
    Scrape all stories with sids.

    :param sids: list of sids in the  form of strings.
    :type sids: list of str.
    :param scrape_reviews: Scrape reviews for a story.
    :type scrape_reviews: bool

    Example:

    .. code-block:: python

                    from ffscraper.phases import phase1
                    phase1(['1', '2', '3', '4'])
    """

    people = set()
    fandoms = set()
    timestamps = []

    for sid in tqdm(sids):

        try:
            current_story = story.scraper(sid, rate_limit=2)
        except Exception:
            continue

        # Push the timestamps onto the heap.
        heappush(timestamps, (int(current_story['published']), 'published'+sid))
        heappush(timestamps, (int(current_story['updated']), 'lastupdated'+sid))

        if scrape_reviews and ('num_reviews' in current_story):
            try:
                reviews = review.scraper(sid, current_story['num_reviews'])
            except Exception:
                print('Error in Reviews!')
                continue

            for entry in reviews:
                # (reviewer, chapter, timestamp, review_text)

                # Push the timestamp onto the heap
                heappush(timestamps, (int(entry[2]), entry[0] + '-rev-' + sid))

                if entry[0] != 'Guest':

                    # Add the reviewer to the set of people.
                    people.add(entry[0])

                review_text = TextBlob(entry[3])
                print(review_text.sentiment)

def phase2():
    """
    Order and process various timestamps.
    """
    pass

def phase3(uids, fandoms=[]):
    """
    Scrape all profiles with uids. Reason about specific fandoms.

    :param uids: list of user-ids.
    :type uids: list of str.
    :param fandoms: list of fandoms (default: [])
    :type fandoms: list of str.
    """
    for uid in tqdm(uids):

        try:
            # Scrape the user's profile.
            current_user = profile.scraper(uid, rate_limit=2)
            # Set variables based on contents of dictionary.
            fav_stories, inverted_favs = current_user['favorite_stories']
            favorite_authors = user_profile['favorite_authors']
        except Exception:
            continue

        for fandom in fandoms:
            relative_score = profile._relative_likes(fav_stories, inverted_favs, fandom)
            # Build Predicates
            pass

        for author in favorite_authors:
            if author in uids:
                # Build predicates
                pass
