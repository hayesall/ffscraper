
#   Copyright (c) 2018-2019 Alexander L. Hayes (@hayesall)
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
from collections import Counter

import argparse

"""
BoostSRL needs negative examples to function correctly (since it is a discrim-
inative learner). Since negative examples do not explicitly exist in this data,
we need to 'halucinate' them based on what is not in the positive examples.

This currently has a hard-coded assumption that the relation of interest is
'liked'. This assumption should be rethought in the future if other targets
may be of interest.

Example usage:

$ head -n 3 posEx.txt
liked("818854","2627916").
liked("794226","2358854").
liked("271295","2370708").
$
$ python create_negatives.py -f posEx.txt
"""

__author__ = 'Alexander L. Hayes (@hayesall)'
__copyright__ = 'Copyright (c) 2018-2019 Alexander L. Hayes'
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

    def parse(predicate_string):
        """
        Source:
        https://github.com/hayesall/Mode-Inference/blob/master/inferModes.py

        License:
        BSD 2-Clause License

        Copyright (c) 2018 Alexander L. Hayes
        All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this
          list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice,
          this list of conditions and the following disclaimer in the documentation
          and/or other materials provided with the distribution.
        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
        FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
        DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
        SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
        OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

        Input a string of the format:
            'father(harrypotter,jamespotter).'
        Returns a list where [0] is the name of the literal and [1] is the
        list of variables in the rule.
            ['father', ['harrypotter', 'jamespotter']]
        """

        predicate_list = predicate_string.replace(' ','').split(')', 1)[0].split('(')
        predicate_list[1] = predicate_list[1].split(',')
        return predicate_list

    # Create some structures which we will use to infer what is false.
    true_examples = {}
    all_authors = []
    all_stories = []

    for example in pos_list:

        pred_list = parse(example)

        author = pred_list[1][0]
        story = pred_list[1][1]

        # Update the structures.
        all_authors.append(author)
        all_stories.append(story)
        true_examples[tuple([author, story])] = True

    # Iterate over all authors and stories. If an author did not write a story,
    # the predicate is false.
    neg_list = []
    for author in all_authors:
        for story in all_stories:

            if not true_examples.get(tuple([author, story])):
                neg_list.append('liked(' + author + ',' + story + ').')

    # The length of the false_examples will be massive. On a set I was experi-
    # menting with, 423 positives resulted in 177,874 negatives.
    return neg_list

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
    parser.add_argument('-o', '--output', type=str, default='o.txt',
        help='Specify where the output file is written to.'
    )

    # Use the argument parser to get the file name and path.
    args = parser.parse_args()

    # Read/split the positive examples.
    with open(args.file, 'r') as p:
        positive_examples = p.read().splitlines()

    # Generate negative examples by observing positive examples.
    negative_examples = HallucinateNegatives(positive_examples)

    # Write the negative examples back to a file.
    with open(args.output, 'w') as n:
        for negative in negative_examples:
            n.write(negative + '\n')
