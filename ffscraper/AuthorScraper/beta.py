
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

def ScrapeBeta(uid, rate_limit=3):
    """
    Scrapes the data from a user's beta profile on FanFiction.Net

    # NOTE: This may be more appropriate as a separate method for scraping
    beta profiles (https://www.fanfiction.net/betareaders/)

    If a user is not a beta reader, their 'beta' page will list a warning
    which reads "[username] is not a registered beta reader."

    @method ScrapeBeta
    @param  {uid}           uid     user id number for a particular user
    @param  {dict}          prof
    """

    # Rate Limit
    time.sleep(rate_limit)

    # Make a request to the site, make a BeautifulSoup instance for the html
    r = requests.get('https://www.fanfiction.net/beta/' + uid)
    html = r.text
    soup = bs(html, 'html.parser')
