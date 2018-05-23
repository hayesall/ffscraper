
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

def PredicateBuilder(predType, *values):
    """
    .. versionadded:: 0.3.0

    Converts inputs into predicates, creating examples and facts in predicate-
    logic format.

    >>> PredicateBuilder('action', 'value1', 'value2')
    action(value1, value2)
    
    .. seealso::
       This function is mostly included for easy conversion to the format used
       by BoostSRL, the learning/inference engine in mind while building this.

       BoostSRL - Boosting for Statistical Relational Learning
       https://github.com/starling-lab/BoostSRL
       https://starling.utdallas.edu/software/boostsrl/
    """
    ret = predType.replace(' ', '') + '('
    for v in values:
        ret += v.replace(' ', '') + ','
    return ret[:-1] + ').'
