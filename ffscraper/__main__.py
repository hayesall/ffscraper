
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

import argparse
import copy

from FanFicScraper import story
from FanFicScraper import review
import Utils

__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache License, Version 2.0'
__version__ = '0.1.2'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'

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

args = parser.parse_args()

if args.version:
    print(__version__)
    exit(0)

if args.sid:
    # Scrape the contents of a single file from FanFiction.Net
    current_story = story.FanfictionScraper(args.sid)

    predicates = []
    predicates.append(Utils.PredicateLogicBuilder('author', current_story['aid'], current_story['sid']))
    predicates.append(Utils.PredicateLogicBuilder('rating', current_story['sid'], current_story['rating']))
    predicates.append(Utils.PredicateLogicBuilder('genre', current_story['sid'], current_story['genre']))

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

    sids = Utils.ImportStoryIDs(args.file)
    # Initialize a remaining_sids list as a copy of sids
    remaining_sids = copy.copy(sids)

    # Values for the progress bar.
    number_of_sids = len(sids)
    counter = 0

    for sid in sids:

        # Helpful progress bar
        Utils.progress(counter, number_of_sids, status='Currently on: {0}...'.format(sid))
        counter += 1

        try:
            current_story = story.FanfictionScraper(sid)
        except:

            # If errors are encountered, alert the user and dump the problematic sid.
            error_file = 'UNKNOWN.txt'

            print('\nEncountered an error while scraping {0}.'.format(sid))
            print('Adding sid to file: {0}'.format(error_file))
            with open(error_file, 'a') as f:
                f.write(sid + '\n')
            continue

        predicates = []
        # schema will be used with cytoscape
        schema = []

        schema.append('user' + current_story['aid'] + ' wrote story' + current_story['sid'])

        predicates.append(Utils.PredicateLogicBuilder('author', current_story['aid'], current_story['sid']))
        predicates.append(Utils.PredicateLogicBuilder('rating', current_story['sid'], current_story['rating']))
        predicates.append(Utils.PredicateLogicBuilder('genre', current_story['sid'], current_story['genre']))

        if current_story.get('Reviewers'):
            reviewers = current_story['Reviewers']

            for reviewer in reviewers:
                predicates.append(Utils.PredicateLogicBuilder('reviewed', reviewer, current_story['sid']))
                schema.append('user' + reviewer + ' reviewed story' + current_story['sid'])

        # Remove the current sid from the list of remaining_sids
        remaining_sids.remove(sid)

        with open(args.output, 'a') as f:
            for p in predicates:
                f.write(p + '\n')

        with open(args.Cout, 'a') as f:
            for p in schema:
                f.write(p + '\n')
