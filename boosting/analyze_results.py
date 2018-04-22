
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

import numpy as np

"""
A short Python script for analyzing the results output from
run_boosting_jobs.sh
"""

__author__ = 'Alexander L. Hayes (@batflyer)'
__copyright__ = 'Copyright (c) 2018 Alexander L. Hayes'
__license__ = 'Apache'
__version__ = '0.0.1'
__maintainer__ = __author__
__email__ = 'alexander@batflyer.net'
__status__ = 'Prototype'

def getValueFromList(value, input_list):

    ret = []

    for line in input_list:
        if value in line:
            ret.append(float(line.split('=')[1]))

    return ret

if  __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='''Analyze the results output by run_boosting_jobs.sh''',
        epilog='''Copyright (c) 2018 Alexander L. Hayes, Distributed under the
                  terms of the Apache 2.0 License. A full copy of the license
                  is available in the base of this repository.'''
    )

    parser.add_argument('-f', '--file', type=str, required=True,
        help='Specify the file to analyze.'
    )
    '''
    parser.add_argument('-a', '--attribute', type=str,
        help='Specify the property to return.'
    )
    '''

    attributes = ['AUCROC', 'AUCPR', 'CLL', 'Precision', 'Recall', 'F1']

    args = parser.parse_args()

    with open(args.file, 'r') as f:
        input_file_list = f.read().splitlines()

    aucroc = getValueFromList('AUC ROC', input_file_list)
    auc_pr = getValueFromList('AUC PR', input_file_list)
    #precision = getValueFromList('Precision', input_file_list)
    recall = getValueFromList('Recall', input_file_list)

    print(np.mean(aucroc))
    print(np.mean(auc_pr))
    print(np.mean(recall))
