
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

import argparse

"""
BoostSRL needs negative examples to function correctly (since it is a discrim-
inative learner). Since negative examples do not explicitly exist in this data,
we need to 'halucinate' them based on what is not in the positive examples.

Example usage:

$ head -n 3 posEx.txt
author("818854","2627916").
author("794226","2358854").
author("271295","2370708").
$
$ python create_negatives.py -f posEx.txt
"""

__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache'
__version__ = '0.0.1'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'

def HallucinateNegatives(pos_list):
    """
    Reads a list of positive examples and returns a list of negative examples
    based on the provided content.

    @method HallucinateNegatives
    @param  {list}  pos_list                list of positive examples
    @return {list}  neg_list                list of negative examples

    Example:
    >>> HallucinateNegatives(['a("1","2").', 'a("3","4").'])
    ['a("1","4").', 'a("3","2").']
    """

    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='''Hallucinate negative examples from positive examples.''',
        epilog='''Copyright (c) 2018 Alexander L. Hayes, Distributed under the
                  terms of the Apache 2.0 License. A full copy of the license is
                  available at the base of this repository.'''
    )

    parser.add_argument('-f', '--file', type=str, required=True,
        help='Specify the file to hallucinate negative examples from.'
    )

    args = parser.parse_args()

    with open(args.file) as f:
        positive_examples = f.read().splitlines()
