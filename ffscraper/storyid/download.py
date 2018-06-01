
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
Build a local copy of the categories and fandoms on FanFiction.Net.
"""

from __future__ import print_function

import json
import sys
import time

from tqdm import tqdm
from ..utils import soupify

def download():
    """
    Download names and addresses for each category and fandom on FanFiction.Net

    .. code-block:: python

                    from ffscraper.storyid.download import download
                    fandoms = download()

                    with open('fandoms.json', 'w') as f:
                        json.dump(fandoms, f, indent=2)
    """

    categories = ['anime', 'book', 'cartoon', 'comic', 'game',
                  'misc', 'play', 'movie', 'tv']

    def download_category(category):
        """
        Download one of the categories.
        """
        soup = soupify('https://www.fanfiction.net/' + category + '/')
        time.sleep(3)

        ahref = soup.find('div', {'id': 'list_output'}).find_all('a')

        for a in ahref:
            try:
                yield a.text, a['href']
            except:
                continue

    fandoms_by_category = {}

    for c in tqdm(categories):

        fandoms_by_category[c] = []
        links = list(download_category(c))

        for l in links:

            fandoms_by_category[c].append({
                'name': l[0],
                'address': 'https://www.fanfiction.net' + l[1]
            })

    return fandoms_by_category
