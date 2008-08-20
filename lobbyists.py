#
# lobbyists.py - Parse and import Senate LD-1/LD-2 XML documents.
# Copyright (C) 2008 Drew Hess <dhess@bothan.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import xml.dom.pulldom
import sqlite3

# Attribute parsers.

def identity(x):
    return x

def amount(x):
    if x == '':
        return None
    else:
        return int(x)
    
def lower(x):
    return x.lower()

def period(x):
    periods = {
        '1st Quarter (Jan 1 - Mar 31)': 'Q1',
        '2nd Quarter (Apr 1 - June 30)': 'Q2',
        '3rd Quarter (July 1 - Sep 30)': 'Q3', 
        '4th Quarter (Oct 1 - Dec 31)': 'Q4', 
        'Mid-Year (Jan 1 - Jun 30)': 'H1',
        'Year-End (July 1 - Dec 31)': 'H2',
        'UNDETERMINED': 'undetermined'
        }
    #if x in periods.keys():
    #    return periods[x]
    #else:
    #    return 'unknown (%s)' % x
    return periods[x]

def optional(x):
    """Returns identity if specified, None if not."""
    if x == '':
        return None
    else:
        return identity(x)


def filings(doc):
    """The sequence of all Filing elements in a lobbyist database.

    doc - The XML document. Can be a filename, a URL or anything else
    that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of expanded DOM Filing elements.

    """
    dom = xml.dom.pulldom.parse(doc)
    for event, node in dom:
        if event == 'START_ELEMENT' and node.nodeName == 'Filing':
            dom.expandNode(node)
            yield node
            

def parse_element(elt, attrs):
    """Return the attributes of a DOM element as a sequence of pairs.

    elt - The DOM element.

    attrs - A sequence of tuples of 3 items each. The first item is
    the attribute name (a string). The second is the identifier
    associated with the parsed attribute value in the yielded
    pair. The third is the parsing function. It's applied to the
    attribute's DOM value, and its output is stored with the
    identifier in the yielded pair.

    Note that attributes which don't appear in the DOM are given to
    the attribute parser as the empty string ('').

    Yields a sequence of (identifier, value) pairs.

    """
    for name, id, parse in attrs:
        yield (id, parse(elt.getAttribute(name)))


filing_attrs = [('ID', 'id', identity),
                ('Year', 'year', int),
                ('Received', 'filing_date', identity),
                ('Amount', 'amount', amount),
                ('Type', 'type', identity),
                ('Period', 'period', period)]


def parse_filings(doc):
    """Iterate over all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    for elt in filings(doc):
        yield dict(parse_element(elt, filing_attrs))


def import_filings(con, filings):
    """Import filings into an sqlite3 database.

    The sqlite3 database is assumed to have a table named "filing"
    with the following column names: "id", "type", "year", "period",
    "filing_date" and "amount". The type of each column should be
    compatible with the Python type of the corresponding value in
    the filing dictionaries.
    
    con - A Connection object for the sqlite3 database.

    filings - A sequence of filing dictionaries. Each dictionary must
    have the following keys: 'id', 'type', 'year', 'period',
    'filing_date' and 'amount'.

    Returns True.
    
    """
    con.executemany('INSERT INTO filing VALUES(\
                       :id, :type, :year, :period, :filing_date, :amount)',
                    filings)
    return True
