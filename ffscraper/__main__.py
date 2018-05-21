
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

# Python Standard Library Modules
from heapq import heappush
from heapq import heappop
import argparse
import copy
import logging
import sys

# Python 2/3 Compatability for Pickling.
if sys.version_info < (3,0,0):
    import cPickle as pickle
else:
    import pickle

from .fanfic import story
from .fanfic import review
from .author import profile
from . import utils

# <Metadata>
__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache License, Version 2.0'
__version__ = '0.3.0-prerelease'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'
# </Metadata>

# <Logging>
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_handler = logging.FileHandler('main_log.log')
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
logger.info('Started logger.')
# </Logging>

# <Argument Parser>
parser = argparse.ArgumentParser(
    description='''Scraper for FanFiction.Net.''',
    epilog='''Copyright (c) 2018 Alexander L. Hayes. Distributed under the
              terms of the Apache 2.0 License. A full copy of the license is
              available at the base of this repository.'''
)

mode = parser.add_mutually_exclusive_group()

mode.add_argument('-s', '--sid', type=str,
    help='Scrape a single story.')
mode.add_argument('-f', '--file', type=str,
    help='Scrape all sids contained in a file.')

parser.add_argument('-V', '--version', action='store_true',
    help='Print the version number, then exit.')
parser.add_argument('-v', '--verbose', action='store_true',
    help='Increase verbosity to help with debugging.')

parser.add_argument('-co', '--Cout', type=str, default='cytoscape.txt',
    help='Set output file for cytoscape network file.')
parser.add_argument('-o', '--output', type=str, default='facts.txt',
    help='Set output file the information scraped.')
# </Argument Parser>

args = parser.parse_args()

def schemaString(a1, a2, a3):
    """
    Return the the arguments as a string for use in Cytoscape.
    """
    return a1 + ' ' + a2 + ' ' + a3

if args.version:
    print(__version__)
    exit(0)

if args.sid:
    # Scrape the contents of a single file from FanFiction.Net
    current_story = story.scraper(args.sid)

    # Create predicates for BoostSRL.
    predicates = []
    predicates.append(utils.PredicateLogicBuilder('author',
                                                  current_story['aid'],
                                                  current_story['sid']))
    predicates.append(utils.PredicateLogicBuilder('rating',
                                                  current_story['sid'],
                                                  current_story['rating']))
    predicates.append(utils.PredicateLogicBuilder('genre',
                                                  current_story['sid'],
                                                  current_story['genre']))
    for p in predicates:
        print(p)

elif args.file:
    # Import the sids from the file and scrape each of them.

    # Initialize the sids as a stack
    sids = utils.ImportStoryIDs(args.file)

    # Initialize the number_of_sids to avoid recalculation and a counter from 0
    number_of_sids = len(sids)
    counter = 0

    # Timestamp heap
    timestamp_heap = []

    # Initialize a set of people, a set of fandoms, and copy the stories.
    people = set()
    fandoms = set()
    stories = copy.copy(sids)

    # Phase I: Scrape stories.
    logger.info('====== Starting Phase I ======')
    logger.info('Beginning loop with ' + str(number_of_sids) + ' stories.')
    while sids:

        # Increment our counter.
        counter += 1

        # Pop the current sid off the stack
        sid = sids.pop()

        # Helpful progress bar
        utils.progress(counter, number_of_sids,
                       status='Scraping: {0}...'.format(sid))

        # Initialize predicates for BoostSRL and schema for Cytoscape.
        predicates = []
        schema = []

        # Try scraping the story. If it fails, log and move on.
        try:
            logger.info('Started scraping sid: ' + sid)
            current_story = story.scraper(sid, rate_limit=1)
            logger.info('Finished scraping sid: ' + sid)

        except Exception:
            # If errors occur, log the exception.
            logger.error('fanfiction.net/s/' + sid, exc_info=True)
            continue

        # Add the timestamps to the timestamp_heap
        heappush(timestamp_heap, (int(current_story['published']),
                                  'published' + sid))
        heappush(timestamp_heap, (int(current_story['updated']),
                                  'lastupdated' + sid))

        # Try scraping reviews for the story. If it fails, log and move on.
        if 'num_reviews' in current_story:
            try:
                logger.info('Scraping reviews for sid: ' + sid)
                current_story_reviews = review.scraper(sid,
                                            current_story['num_reviews'],
                                            rate_limit=1)
                logger.info('Finished reviews for sid: ' + sid)
            except Exception:
                logger.error('Review: /s/' + sid, exc_info=True)
                continue

            for entry in current_story_reviews:
                # (reviewer, chapter, timestamp, review_text)

                heappush(timestamp_heap, (int(entry[2]),
                                         'reviewed' + sid))

                # Write the review_text to a file
                with open('review_text.txt', 'a') as f:
                    f.write('[' + entry[0] + ',' + sid + '] ' + entry[3] + '\n')

                if entry[0] != 'Guest':
                    # Add the reviewer to the set of people.
                    people.add(entry[0])

                    predicates.append(
                        utils.PredicateLogicBuilder('reviewed',
                                                    entry[0],
                                                    current_story['sid']))
                    schema.append(
                        schemaString('user' + entry[0],
                                     'reviewed',
                                     'story' + current_story['sid']))


        # Add the author of the current story to the set of people.
        people.add(current_story['aid'])
        # Add the current fandom to the set of fandoms.
        fandoms.add(current_story['fandom'])

        # Create a schema list for Cytoscape.
        schema.append(schemaString('user' + current_story['aid'],
                                   'wrote',
                                   'story' + current_story['sid']))

        # Create predicates for BoostSRL.
        predicates.append(utils.PredicateLogicBuilder('author',
                                                      current_story['aid'],
                                                      current_story['sid']))
        predicates.append(utils.PredicateLogicBuilder('rating',
                                                      current_story['sid'],
                                                      current_story['rating']))
        predicates.append(utils.PredicateLogicBuilder('genre',
                                                      current_story['sid'],
                                                      current_story['genre']))

        """
        if current_story.get('Reviewers'):

            # Add reviewers to the set of people.
            people = people.union(set(current_story['Reviewers']))

            # Create associated predicates and Cytoscape schemas.
            for reviewer in current_story['Reviewers']:
                predicates.append(
                    utils.PredicateLogicBuilder('reviewed',
                                                reviewer,
                                                current_story['sid'])
                    )
                schema.append(schemaString('user' + reviewer,
                                           'reviewed',
                                           'story' + current_story['sid']))
        """

        with open(args.output, 'a') as f:
            for p in predicates:
                f.write(p + '\n')
        with open(args.Cout, 'a') as f:
            for p in schema:
                f.write(p + '\n')

    logger.info('====== Starting Phase II ======')
    logger.info('Popping timestamps from the timestamp_heap:')

    with open('timestamps.txt', 'w') as f:
        for _ in range(len(timestamp_heap)):
            action = heappop(timestamp_heap)
            f.write(str(action[0]) + ' ' + action[1] + '\n')

    logger.info('====== Starting Phase III ======')
    logger.info('Encountered ' + str(len(fandoms)) +
                ' fandom(s) during Phase I.')
    logger.info('Fandoms encountered: ' + str(fandoms))
    logger.info('Encountered ' + str(len(people)) +
                ' user(s) during Phase I.')
    # Phase II: User Profiles from the set of users observed during Phase I.
    # Initialize the number_of_sids to avoid recalculation and a counter from 0
    number_of_uids = len(people)
    counter = 0

    # Create a copy of people. The original one will be mutated.
    authors_and_reviewers = copy.copy(people)
    while people:

        # Increment our counter.
        counter += 1

        # Pop the current person from the set of people.
        uid = people.pop()

        # Helpful progress bar
        utils.progress(counter, number_of_uids,
                       status='Scraping: {0}...'.format(uid))

        # Try scraping the profile, log if/where the scraper throws errors.
        try:
            logger.info('Started scraping uid: ' + uid)

            # profile.scraper returns a dictionary of user information.
            user_profile = profile.scraper(uid, rate_limit=1)

            # Accessing that dictionary gets favorite stories, authors, etc.
            fav_stories, inverted_favs = user_profile['favorite_stories']
            favorite_authors = user_profile['favorite_authors']

            """
            fav_stories, inverted_favs = profile.scraper(
                                        uid, rate_limit=1)['favorite_stories']
            """
            logger.info('Finished scraping uid: ' + uid)
        except Exception:
            # If errors occur, log the exception and continue.
            logger.error('fanfiction.net/u/' + uid, exc_info=True)
            continue

        # Initialize predicates for BoostSRL and schema for Cytoscape.
        predicates = []
        schema = []

        # Estimate how much the user likes each fandom scraped from.
        for fandom in fandoms:
            relative_score = profile._relative_likes(fav_stories,
                                                     inverted_favs, fandom)

            logger.info('user/fandom: ' + uid + '/' + fandom + ': ' +
                        str(relative_score))

            if fandom in inverted_favs:
                for sid in inverted_favs[fandom]:
                    if sid in stories:
                        predicates.append(
                            utils.PredicateLogicBuilder('liked', uid, sid))
                        schema.append(
                            schemaString('user' + uid, 'liked', 'story' + sid))

        # Create predicates for the user's favorite authors if those authors
        # were observed during this session.
        for author in favorite_authors:
            if author in authors_and_reviewers:
                predicates.append(
                    utils.PredicateLogicBuilder('favoriteAuthor', uid, author))
                schema.append(
                    schemaString('user' + uid, 'favAuthor', 'user' + author))

        with open(args.output, 'a') as f:
            for p in predicates:
                f.write(p + '\n')
        with open(args.Cout, 'a') as f:
            for p in schema:
                f.write(p + '\n')

# Shut down the logger and exit with no errors.
logger.info('Reached bottom of file, shutting down logger.')
logging.shutdown()
exit(0)
