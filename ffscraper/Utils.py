
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

def PredicateLogicBuilder(type, id, value):
    """
    Converts inputs into (id, value) pairs, creating positive examples
    and facts in predicate-logic format.

    @method PredicateLogicBuilder
    @param  {str}   type                type of the predicate
    @param  {str}   id                  identifier attribute
    @param  {str}   value               value of the identifier
    @return {str}   ret                 string of the form 'A(B,C).'

    Example:
    >>> f = RelationalPredicateLogic('author', '123', '456')
    >>> print(f)
    author("123","456").
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

def ImportStoryIDs(path_to_file):
    """
    Reads FanFiction.Net story-ids from a file, where each story-id is on
    a separate line. Returns a list of strings representing story-ids.

    @method ImportStoryIDs
    @param  {str}               path_to_file    path to sid file.
    @return {list}              sids            list of strings (sids)

    Example:
    $ cat sids.txt
    123
    344
    $ python
    >>> import FanfictionScraper as fs
    >>> sids = fs.ImportStoryIDs('sids.txt')
    >>> sids
    ['123', '344']
    """

    with open(path_to_file) as f:
        sids = f.read().splitlines()

    return sids

if __name__ == '__main__':

    raise(Exception('No main class in Utils.py'))
    exit(1)
