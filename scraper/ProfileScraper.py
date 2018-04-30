
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

from bs4 import BeautifulSoup as bs

import requests
import time

__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache'
__version__ = '0.0.1'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'

"""
A user's profile on FanFiction.Net may consist of some combination of a:
        1. uid (integer)
        2. username (string)
        3. beta profile (bool)
        4. My Stories
        5. Favorite Stories
        6. Favorite Authors
        7. Communities

Beta profile users additionally have additional properties:
    Beta Description:
        1. Beta Bio (general description as a beta reader)
        2. My Strengths (beta, writing, or reading strength)
        3. My Weaknesses (beta, writing, or reading weaknesses)
        4. Preferred (types of stories I prefer over others)
        5. Would Rather Not (I do not beta read for these stories)

    Beta Preferences:
        1. Language
        2. Content Rating (range of acceptable fiction ratings)
        3. Categories (categories in black are ones this beta has authored for)
        4. Genres (genres in black are ones this beta has authored for)

In practice, the 'My Stories' section is likely to be duplicate information
when FanfictionScraper.py already picks this information up.
"""

class Profile:

    def __init__(self, uid):
        self.uid = uid
        pass

    def ScrapeProfile(self):
        pass

    def ScrapeBeta(self):
        pass

if __name__ == '__main__':
    exit(0)
