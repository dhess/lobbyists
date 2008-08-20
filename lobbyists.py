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
            

def child_elements(elt):
    """Yield a sequence of child elements of the given DOM element."""
    for child in elt.childNodes:
        if child.nodeType == xml.dom.Node.ELEMENT_NODE:
            yield child
            
        
def parse_attrs(elt, attrs):
    """Parse the attributes of a DOM element into a sequence of pairs.

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


def parse_registrant(elt):
    """Parse a Registrant DOM element.

    elt - The Registrant DOM element.

    Returns a list with one item, a pair whose first item is the
    string 'registrant' and whose second item is the dictionary of
    parsed attributes.

    """
    # Caller expects a sequence.
    return [('registrant', dict(parse_attrs(elt, registrant_attrs)))]
    

def element_name(elt):
    return elt.tagName


filing_attrs = [('ID', 'id', identity),
                ('Year', 'year', int),
                ('Received', 'filing_date', identity),
                ('Amount', 'amount', amount),
                ('Type', 'type', identity),
                ('Period', 'period', period)]

registrant_attrs = [('Address', 'address', optional),
                    ('GeneralDescription', 'description', optional),
                    ('RegistrantCountry', 'country', identity),
                    ('RegistrantID', 'senate_id', int),
                    ('RegistrantName', 'name', identity),
                    ('RegistrantPPBCountry', 'ppb_country', identity)]

subelt_parsers = {
    'Registrant': parse_registrant
    }

def parse_filings(doc):
    """Parse all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    for filing_elt in filings(doc):
        filing = dict(parse_attrs(filing_elt, filing_attrs))
        for elt in child_elements(filing_elt):
            parser = subelt_parsers[element_name(elt)]
            filing.update(parser(elt))
        yield filing


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
