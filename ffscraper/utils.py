
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

import sys

"""
+-------------+--------------------------------------------------+
|   **Name**  |               **Description**                    |
+-------------+--------------------------------------------------+
|   Utils.py  | Module with some helpful utilities for ffscraper |
+-------------+--------------------------------------------------+
"""


def ImportStoryIDs(path_to_file):
    """
    .. versionadded:: 0.1.0

    Reads FanFiction.Net story-ids from a file, where each story-id is on
    a separate line. Returns a list of strings representing story-ids.

    :param path_to_file: path to a file containing story-ids from
                         FanFiction.Net, where each story-id is
                         contained on a newline.
    :type path_to_file: str.
    :returns: A list of strings representing the story-ids.
    :rtype: list of strings.

    Example:

    .. code-block:: python

                    # File: example.py
                    import ffscraper as ffs

                    # Story-ids in this example are stored in a text file.
                    sids = ffs.utils.ImportStoryIDs('data/Coraline/sids.txt')
                    print(sids)

    .. code-block:: bash

                    $ cat data/Coraline/sids.txt
                    123
                    344
                    $ python example.py
                    ['123', '344']

    .. warning::
       This function was designed and tested with Unix-style paths and
       end-of-line characters in mind, these have not been tested thoroughly
       on Windows.
    """

    with open(path_to_file) as f:
        sids = f.read().splitlines()

    return sids


def soupify(url):
    """
    .. versionadded:: 0.3.0

    Helper function for returning the soup from a url.

    :param url: A url to a web address.
    :type url: str.

    :returns: Beautiful Soup html parser for the text at the url.
    :rtype: bs4.BeautifulSoup class

    .. code-block:: python

                    import ffscraper as ffs

                    soup = ffs.utils.soupify('https://www.fanfiction.net/u/12')
    """

    from bs4 import BeautifulSoup as bs
    import requests

    html = requests.get(url).text
    return bs(html, 'html.parser')
