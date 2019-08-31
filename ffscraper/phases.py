
# -*- coding: utf-8 -*-

#   Copyright (c) 2018-2019 Alexander L. Hayes (@hayesall)
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

# Relative imports from ffscraper
from .author import profile
from .fanfic import story
from .fanfic import review
from .format import format
from . import storyid

# Non-Standard Library Modules
from textblob import TextBlob
from tqdm import tqdm

# Python Standard Library Modules
from heapq import heappush
from heapq import heappop
import copy
import logging
import sys

# Python 2/3 Compatability for Pickling.
if sys.version_info < (3, 0, 0):
    import cPickle as pickle
else:
    import pickle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler('ffscraper_log.log')
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('Started logger.')


def phase0(fandom, max_pages=float('inf'), rate_limit=3, log=False):
    """
    Scrape story-ids for a particular fandom.

    :param fandom: The identifier on FanFiction.Net pointing to a specific
                   community. e.g. '/book/Harry-Potter/'
    :type fandom: str.

    Example:

    .. code-block:: python

                    from ffscraper.phases import phase0

                    sids = phase0('/book/Harry-Potter/')

    .. code-block:: python

                    from ffscraper.phases import phase0

                    sids = phase0('/book/Coraline/', max_pages=3)

    # IDEA: Limit how many stories are returned (for instance, I may want
            the 25 most recently-updated stories).

    General notes on how filters may be applied in order to tailor the stories
    one is looking for:

    Sorting Methods
    ---------------
    Update Date: &srt=1 (most recent first)
    Publish Date: &srt=2 (most recent first)
    Reviews: &srt=3 (most to least)
    Favorites: &srt=4
    Follows: &srt=5

    Fiction Rating
    --------------
    All: &r=10
    K-T: &r=103
    K-K+: &r=102
    K: &r=1
    K+: &r=2
    T: &r=3
    M: &r=4

    Status
    ------
    In Progress: &s=1
    Complete: &s=2

    Language
    --------
    English: &lan=1

    """
    url = 'https://www.fanfiction.net' + fandom
    return storyid.scrape(url, max_pages=max_pages, rate_limit=rate_limit)



def phase1(sids, output_file='facts.txt', scrape_reviews=True, log=True):
    """
    Scrape all stories with sids.

    :param sids: list of sids in the form of strings.
    :type sids: list of str.
    :param scrape_reviews: Scrape reviews for a story.
    :type scrape_reviews: bool
    :param verbose: Log to a file.

    Example:

    .. code-block:: python

                    from ffscraper.phases import phase1

                    # Return sets of people, fandoms; and a heap of timestamps.
                    p, f, t = phase1(['1', '2', '3', '4'], log=True)

    .. code-block:: bash

                    100%|█████████████████████| 4/4 [00:21<00:00,  3.00s/it]

    """

    if log:
        logger.info('====== Starting Phase I ======')
        logger.info('Beginning loop with ' + str(len(sids)) + ' stories.')

    # Initialize lists for storing predicates and schema (write to disk).
    predicates = []

    # These three will be returned for use in later phases.
    people = set()
    fandoms = set()
    timestamps = []

    for sid in tqdm(sids):

        try:
            if log:
                logger.info('Scraping sid: ' + sid)
            Story = story.scraper(sid, rate_limit=2)
            if log:
                logger.info('Finished sid: ' + sid)
        except Exception:
            if log:
                logger.error('fanfiction.net/s/' + sid, exc_info=True)
            continue

        # Push the timestamps onto the heap.
        heappush(timestamps,
                 (int(Story['published']),
                  'published'+sid))
        heappush(timestamps,
                 (int(Story['updated']),
                  'lastupdated'+sid))

        # Add people and fandoms to the appropriate sets.
        people.add(Story['aid'])
        fandoms.add(Story['fandom'])

        if scrape_reviews and ('num_reviews' in Story):
            try:
                if log:
                    logger.info('Scraping reviews: ' + sid)
                reviews = review.scraper(sid, Story['num_reviews'],
                                         rate_limit=2)
                if log:
                    logger.info('Finished reviews: ' + sid)
            except Exception:
                if log:
                    logger.error('Review: /s/' + sid, exc_info=True)
                continue

            for entry in reviews:
                # (reviewer, chapter, timestamp, review_text)

                # Push the timestamp onto the heap
                heappush(timestamps, (int(entry[2]), entry[0] + '_rev_' + sid))

                # Get the review text to evaluate sentiment.
                review_text = TextBlob(entry[3])
                if log:
                    logger.info('[' + entry[0] + ',' + sid + '] ' +
                                str(review_text.sentiment))

                if entry[0] != 'Guest':
                    # Add the reviewer to the set of people.
                    people.add(entry[0])
                    predicates.append(format('reviewed', entry[0],
                                             Story['sid'],
                                             predicate=True)['predicate'])

        predicates.append(format('author', Story['aid'], Story['sid'],
                                 predicate=True)['predicate'])
        predicates.append(format('rating', Story['sid'], Story['rating'],
                                 predicate=True)['predicate'])
        predicates.append(format('genre', Story['sid'], Story['genre'],
                                 predicate=True)['predicate'])

        with open(output_file, 'a') as f:
            for p in predicates:
                f.write(p + '\n')

    if log:
        logger.info('Encountered ' + str(len(fandoms)) + ' fandom(s).')
        logger.info('Fandom(s) found: ' + str(fandoms))
        logger.info('Encountered ' + str(len(people)) + ' people.')
        logger.info('====== Ending Phase I ======')
    return people, fandoms, timestamps


def phase2(timestamps, log=False):
    """
    Order and process various timestamps.

    This does not really make sense as a "Phase", since nothing is scraped.

    I have not quite figured out how best to handle these, perhaps create the
    ordering by popping from the stack, but returning as a dictionary or as a
    more powerful data structure for querying certain events which occurred
    on, before, or after a certain date?
    """

    # Make a copy of timestamps to help prevent some pass-by-object-reference
    # that may cause confusion if not addressed like this.
    t = copy.copy(timestamps)

    if log:
        logger.info('====== Starting Phase II ======')

    with open('timestamps.txt', 'w') as f:
        for _ in range(len(t)):
            action = heappop(t)
            f.write(str(action[0]) + ' ' + action[1] + '\n')

    if log:
        logger.info('====== Ending Phase II ======')


def phase3(uids, sids, output_file='facts.txt', fandoms=[], log=True):
    """
    Scrape all profiles with uids, checking for specific storyids.
    Reason about specific fandoms.

    :param uids: list of user-ids.
    :type uids: list of str.
    :param fandoms: list of fandoms (default: [])
    :type fandoms: list of str.
    """

    if log:
        logger.info('====== Starting Phase III ======')

    for uid in tqdm(uids):

        try:
            if log:
                logger.info('Started scraping uid: ' + uid)

            # Scrape the user's profile.
            current_user = profile.scraper(uid, rate_limit=2)

            # Set variables based on contents of dictionary.
            fav_stories, inverted_favs = current_user['favorite_stories']
            favorite_authors = current_user['favorite_authors']

            if log:
                logger.info('Finished scraping uid: ' + uid)
        except Exception:
            if log:
                logger.error('fanfiction.net/u/' + uid, exc_info=True)
            continue

        # Initialize predicates for BoostSRL.
        predicates = []

        # Estimate how much the user likes each fandom scraped from.
        for fandom in fandoms:
            relative_score = profile._relative_likes(fav_stories,
                                                     inverted_favs,
                                                     fandom)
            if log:
                logger.info('user/fandom: ' + uid + '/' + fandom + ': ' +
                            str(relative_score))

            if fandom in inverted_favs:
                for sid in inverted_favs[fandom]:
                    if sid in sids:
                        predicates.append(format('liked', uid, sid,
                                                 predicate=True)['predicate'])

        # Create predicates for the user's favorite authors if those
        # authors were observed during this session.
        for author in favorite_authors:
            if author in uids:
                predicates.append(format('favoriteAuthor', uid, author,
                                         predicate=True)['predicate'])

        with open(output_file, 'a') as f:
            for p in predicates:
                f.write(p + '\n')
