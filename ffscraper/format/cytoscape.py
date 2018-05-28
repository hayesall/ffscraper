
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

def cytoscapeFormat(predType, val1, val2):
    """
    .. versionadded:: 0.3.0

    Converts inputs into the triples format used by Cytoscape.

    :param predType: The action which relates one or more values.
    :type predType: str.
    :param val1: The first value.
    :type val1: str.
    :param val2: The second value.
    :type val2: str.

    Cytoscape is mostly built around binary predicates: two entities (nodes)
    connected by a relation (edge). Because hyperedges are not implicitly
    built-in, this function requires three parameters.

    >>> cytoscapeFormat('action', 'value1', 'value2')
    'value1 action value2'

    >>> cytoscapeFormat('friends', 'harry', 'ron')
    'harry friends ron'

    >>> cytoscapeFormat('liked', 'person1', 'story3')
    'person1 liked story3'

    If the outputs of this function are written to a file, it may be imported
    to Cytoscape as follows:

    1. ``File > Import > Network > File`` (choose where you wrote the file).
    2. ``Advanced Options``: Select 'Space', Uncheck 'Use first line as column
       names'
    3. Set ``Column 1`` as ``Source Node`` (green circle).
    4. Set ``Column 2`` as ``Interaction Type`` (violet triangle).
    5. Set ``Column 3`` as ``Target Node`` (red target).
    6. Click 'Ok'

    .. seealso::

       "Cytoscape is an open source software platform for visualizing complex
       networks and integrating these with any type of attribute data."

       The desktop version of Cytoscape includes an option to import a network
       ``File > Import > Network > File``. This function may be used to create
       such files for visualization.

       http://www.cytoscape.org/

    """
    return val1.replace(' ', '') + ' ' + \
           predType.replace(' ','') + ' ' + \
           val2.replace(' ','')
