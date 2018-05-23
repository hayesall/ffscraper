
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

# Non-Standard Library Modules
from textblob import TextBlob
from tqdm import tqdm

# Relative imports from ffscraper
from .fanfic import story
from .fanfic import review
from .author import profile
from . import utils

# Phase I: Scraping stories

def StoryScraping(*sids):
    """
    """
    scrape_reviews = True

    for sid in tqdm(sids):

        try:
            current_story = story.scraper(sid, rate_limit=2)
        except Exception:
            continue

        if scrape_reviews and ('num_reviews' in current_story):
            try:
                reviews = review.scraper(sid, current_story['num_reviews'])
            except Exception:
                print('Error in Reviews!')
                continue

            for entry in reviews:
                # (reviewer, chapter, timestamp, review_text)

                review_text = TextBlob(entry[3])
                print(review_text.sentiment)
