
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
from . import Utils

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
mode.add_argument('-r', '--review', type=str,
    help='Scrape the reviews for a particular story.')

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
    predicates.append(Utils.PredicateLogicBuilder('author',
                                                  current_story['aid'],
                                                  current_story['sid']))
    predicates.append(Utils.PredicateLogicBuilder('rating',
                                                  current_story['sid'],
                                                  current_story['rating']))
    predicates.append(Utils.PredicateLogicBuilder('genre',
                                                  current_story['sid'],
                                                  current_story['genre']))
    for p in predicates:
        print(p)

elif args.review:
    # !!! In progress

    raise(Exception('Review has some bugs, it needs the story metadata.'))
    exit(1)

    ReviewScraper(args.review, 16)
    exit()

elif args.file:
    # Import the sids from the file and scrape each of them.

    # Initialize the sids as a stack
    sids = Utils.ImportStoryIDs(args.file)

    # Initialize the number_of_sids to avoid recalculation and a counter from 0
    number_of_sids = len(sids)
    counter = 0

    # Initialize a set of people.
    people = set()

    while sids:

        # Pop the current sid off the stack
        sid = sids.pop()

        # Helpful progress bar
        Utils.progress(counter, number_of_sids,
                       status='Scraping: {0}...'.format(sid))

        # Try scraping the story. If it fails, log and move on.
        try:
            logger.info('Started scraping sid: ' + sid)
            current_story = story.scraper(sid, rate_limit=1)
            logger.info('Finished scraping sid: ' + sid)
        except Exception:
            # If errors occur, log the exception.
            logger.error('fanfiction.net/s/' + sid, exc_info=True)
            continue

        # Add the author of the current story to the set of people.
        people.add(current_story['aid'])

        # Initialize predicates for BoostSRL and schema for Cytoscape.
        predicates = []
        schema = []

        # Create a schema list for Cytoscape.
        schema.append(schemaString('user' + current_story['aid'],
                                   'wrote',
                                   'story' + current_story['sid']))

        # Create predicates for BoostSRL.
        predicates.append(Utils.PredicateLogicBuilder('author',
                                                      current_story['aid'],
                                                      current_story['sid']))
        predicates.append(Utils.PredicateLogicBuilder('rating',
                                                      current_story['sid'],
                                                      current_story['rating']))
        predicates.append(Utils.PredicateLogicBuilder('genre',
                                                      current_story['sid'],
                                                      current_story['genre']))

        if current_story.get('Reviewers'):

            # Add reviewers to the set of people.
            people = people.union(set(current_story['Reviewers']))

            # Create associated predicates and Cytoscape schemas.
            for reviewer in current_story['Reviewers']:
                predicates.append(
                    Utils.PredicateLogicBuilder('reviewed',
                                                reviewer,
                                                current_story['sid'])
                    )
                schema.append(schemaString('user' + reviewer,
                                           'reviewed',
                                           'story' + current_story['sid']))

        with open(args.output, 'a') as f:
            for p in predicates:
                f.write(p + '\n')
        with open(args.Cout, 'a') as f:
            for p in schema:
                f.write(p + '\n')

        # increment our counter
        counter += 1

# Shut down the logger and exit with no errors.
logger.info('Reached bottom of file, shutting down logger.')
logging.shutdown()
exit(0)
