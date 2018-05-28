
# -*- coding: utf-8 -*-

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
import copy
import logging
import sys

# Python 2/3 Compatability for Pickling.
if sys.version_info < (3,0,0):
    import cPickle as pickle
else:
    import pickle

# Non-Standard Library Modules
from textblob import TextBlob
from tqdm import tqdm

# Relative imports from ffscraper
from .fanfic import story
from .fanfic import review
from .author import profile
from . import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler('ffscraper_log.log')
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('Started logger.')

# Phase I: Scraping stories

def phase1(sids, scrape_reviews=True, log=False):
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

    people = set()
    fandoms = set()
    timestamps = []

    for sid in tqdm(sids):

        try:
            if log:  logger.info('Scraping sid: ' + sid)
            current_story = story.scraper(sid, rate_limit=2)
            if log:  logger.info('Finished sid: ' + sid)
        except Exception:
            if log:  logger.error('fanfiction.net/s/' + sid, exc_info=True)
            continue

        # Push the timestamps onto the heap.
        heappush(timestamps, (int(current_story['published']), 'published'+sid))
        heappush(timestamps, (int(current_story['updated']), 'lastupdated'+sid))

        # Add people and fandoms to the appropriate sets.
        people.add(current_story['aid'])
        fandoms.add(current_story['fandom'])

        if scrape_reviews and ('num_reviews' in current_story):
            try:
                if log:  logger.info('Scraping reviews: ' + sid)
                reviews = review.scraper(sid, current_story['num_reviews'])
                if log:  logger.info('Finished reviews: ' + sid)
            except Exception:
                if log:  logger.error('Review: /s/' + sid, exc_info=True)
                continue

            for entry in reviews:
                # (reviewer, chapter, timestamp, review_text)

                # Push the timestamp onto the heap
                heappush(timestamps, (int(entry[2]), entry[0] + '_rev_' + sid))

                # Get the review text to evaluate sentiment.
                review_text = TextBlob(entry[3])
                if log:  logger.info('[' + entry[0] + ',' + sid + ']' + \
                                     str(review_text.sentiment))

                if entry[0] != 'Guest':
                    # Add the reviewer to the set of people.
                    people.add(entry[0])

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

    if log:  logger.info('====== Starting Phase II ======')

    for _ in range(len(t)):
        action = heappop(t)
        print(str(action[0]) + ' ' + action[1])

    if log:  logger.info('====== Ending Phase II ======')

def phase3(uids, fandoms=[], log=False):
    """
    Scrape all profiles with uids. Reason about specific fandoms.

    :param uids: list of user-ids.
    :type uids: list of str.
    :param fandoms: list of fandoms (default: [])
    :type fandoms: list of str.
    """

    if log:  logger.info('====== Starting Phase III ======')

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
