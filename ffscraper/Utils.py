
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

    >>> from ffscraper.Utils import ImportStoryIDs
    >>> sids = ffs.Utils.ImportStoryIDs('data/Coraline/sids.txt')
    >>> print(sids)
    ['123', '344']

    .. warning::
       This function was designed and tested with Unix-style paths and
       end-of-line characters in mind, these have not been tested thoroughly
       on Windows.
    """

    with open(path_to_file) as f:
        sids = f.read().splitlines()

    return sids

def PredicateLogicBuilder(type, id, value):
    """
    .. versionadded:: 0.1.0

    Converts inputs into (id, value) pairs, creating positive examples
    and facts in predicate-logic format.

    :param type: type of the predicate
    :type type: str.
    :param id: identifier attribute
    :type id: str.
    :param value: value of the identifier
    :type value: str.
    :returns: A string of the form 'A("B","C").'
    :rtype: str.

    Example:

    >>> from ffscraper.Utils import PredicateLogicBuilder
    >>> f = PredicateLogicBuilder('author', '123', '456')
    >>> print(f)
    author("123","456").

    .. note::
       This will likely be changed in future versions, instead of using an
       ``id`` and optional ``value``, these will be rebuilt using \*args.

    .. seealso::
       This function is mostly included for easy conversion to the format used
       by BoostSRL, the learning and inference engine in mind while building
       this.

       BoostSRL - Boosting for Statistical Relational Learning
       https://github.com/starling-lab/BoostSRL
       https://starling.utdallas.edu/software/boostsrl/
    """

    ret = ''

    if value:
        ret += type
        ret += '("'
        ret += id.replace(' ', '')
        ret += '","'
        ret += value.replace(' ', '')
        ret += '").'
    else:
        ret += type
        ret += '("'
        ret += id.replace(' ', '')
        ret += '").'

    return ret

import sys

def progress(count, total, status=''):
    """
    .. versionadded:: 0.1.0

    A helpful progress bar to help deter the insanity that builds inside you
    when you have no idea how long something will take. Distributed under the
    terms of the MIT License by Vladimir Ignatev.

    Based on the GitHub gist:
    https://gist.github.com/vladignatyev/06860ec2040cb497f0f3

    :param count: The number of items completed.
    :type count: int.
    :param total: The total number of items.
    :type total: int.
    :param status: Optional message to display along with the progress bar.
    :type status: str.

    Example:

    >>> from ffscraper.Utils import progress
    >>> from time import sleep
    >>> for i in range(1,10):
    ...     sleep(1)
    ...     progress(i,10)
    ...
    [=====---------------------------------------------] 10.0% ...
    >>>

    .. seealso::
       The MIT License (MIT)
       Copyright (c) 2016 Vladimir Ignatev

       Permission is hereby granted, free of charge, to any person obtaining
       a copy of this software and associated documentation files (the "Software"),
       to deal in the Software without restriction, including without limitation
       the rights to use, copy, modify, merge, publish, distribute, sublicense,
       and/or sell copies of the Software, and to permit persons to whom the Software
       is furnished to do so, subject to the following conditions:

       The above copyright notice and this permission notice shall be included
       in all copies or substantial portions of the Software.

       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
       INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
       PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
       FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
       OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
       OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.1 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

if __name__ == '__main__':

    raise(Exception('No main class in Utils.py'))
    exit(1)
