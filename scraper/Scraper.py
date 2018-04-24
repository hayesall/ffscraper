
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

# progress.py is used under the terms of the MIT license
from progress import progress

import argparse
import re
import requests
import time

from FanfictionScraper import FanfictionScraper
from ReviewScraper import ReviewScraper
from Utils import *

__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache'
__version__ = '0.0.1'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'

if __name__ == '__main__':

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

    args = parser.parse_args()

    if args.sid:
        # Scrape the contents of a single file from FanFiction.Net
        story = FanfictionScraper(args.sid)

        predicates = []
        predicates.append(PredicateLogicBuilder('author', story['aid'], story['sid']))
        predicates.append(PredicateLogicBuilder('rating', story['sid'], story['rating']))
        predicates.append(PredicateLogicBuilder('genre', story['sid'], story['genre']))

        for p in predicates:
            print(p)

    elif args.review:
        # !!! In progress

        ReviewScraper(args.review, 16)
        exit()

    elif args.file:
        # Import the sids from the file and scrape each of them.

        sids = ImportStoryIDs(args.file)

        # Values for the progress bar.
        number_of_sids = len(sids)
        counter = 0

        for sid in sids:

            # Helpful progress bar
            progress(counter, number_of_sids, status='Currently on: {0}'.format(sid))
            counter += 1

            story = FanfictionScraper(sid)

            predicates = []
            predicates.append(PredicateLogicBuilder('author', story['aid'], story['sid']))
            predicates.append(PredicateLogicBuilder('rating', story['sid'], story['rating']))
            predicates.append(PredicateLogicBuilder('genre', story['sid'], story['genre']))

            with open('facts.txt', 'a') as f:
                for p in predicates:
                    f.write(p + '\n')
