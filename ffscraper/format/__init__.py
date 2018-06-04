
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

from .cytoscape import cytoscapeFormat
from .predicate import predicateFormat

from mysql.connector import errorcode
import mysql.connector
import os

config = {
    'user': 'fanfictionuser',
    'password': os.environ.get('FANFICTION_DB_PWD'),
    'host': '127.0.0.1',
    'database': 'fanfictiondb',
    'raise_on_warnings': True
}

try:
    cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with the user name or password.')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('Database does not exist.')
    else:
        print(err)
else:
    cnx.close()


def format(predType, *values, **formats):
    """
    .. versionadded:: 0.3.0

    Abstract function for converting inputs into one or more schema.

    :param predType: Type of the relation.
    :type predType: str.
    :param \*values: Strings representing objects in the relation.
    :type \*values: str.
    :param \*\*formats: Formats to convert the input to.
    :type \*\*formats: bool.

    :returns: Dictionary mapping the \*\*formats values to their output values.
    :rtype: dict.

    .. code-block:: python

                    from ffscraper.format import format

                    # Formats available: cytoscape, predicate
                    formats = format('friends', 'harry', 'ron',
                                     cytoscape=True, predicate=True)

                    for f in formats:
                        print(f, formats[f])

    .. code-block:: bash

                    predicate friends("harry","ron")
                    cytoscape harry friends ron

    """

    structures = {}

    if 'predicate' in formats:

        structures['predicate'] = predicateFormat(predType, *values)

    if 'cytoscape' in formats:

        if len(values) == 2:
            # Detailed explanation in cytoscape.py
            structures['cytoscape'] = cytoscapeFormat(predType, *values)
        else:
            raise(Exception('Cytoscape requires exactly two arguments.'))

    return structures
