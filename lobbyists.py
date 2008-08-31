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
    return periods[x]

def optional(x):
    """Returns identity if specified, None if not."""
    if x == '':
        return None
    else:
        return identity(x)


def filing_elements(doc):
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


def parse_element(elt, id, attrs):
    # Caller expects a sequence
    return [(id, dict(parse_attrs(elt, attrs)))]


registrant_attrs = [('Address', 'address', optional),
                    ('GeneralDescription', 'description', optional),
                    ('RegistrantCountry', 'country', identity),
                    ('RegistrantID', 'senate_id', int),
                    ('RegistrantName', 'name', identity),
                    ('RegistrantPPBCountry', 'ppb_country', identity)]

def parse_registrant(elt):
    """Parse a Registrant DOM element.

    elt - The Registrant DOM element.

    Returns a list with one item, a pair whose first item is the
    string 'registrant' and whose second item is the dictionary of
    parsed attributes.

    """
    return parse_element(elt, 'registrant', registrant_attrs)


filing_attrs = [('ID', 'id', identity),
                ('Year', 'year', int),
                ('Received', 'filing_date', identity),
                ('Amount', 'amount', amount),
                ('Type', 'type', identity),
                ('Period', 'period', period)]

def parse_filing(elt):
    """Parse a Filing DOM element.

    elt - The Filing DOM element.

    Returns a list with one item, a pair whose first item is the
    string 'filing' and whose second item is the dictionary of parsed
    attributes.

    """
    return parse_element(elt, 'filing', filing_attrs)


def element_name(elt):
    return elt.tagName


subelt_parsers = {
    'Registrant': parse_registrant
    }

def parse_filings(doc):
    """Parse all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    for filing_elt in filing_elements(doc):
        filing = dict(parse_filing(filing_elt))
        for elt in child_elements(filing_elt):
            parser = subelt_parsers[element_name(elt)]
            filing.update(parser(elt))
        yield filing


# XXX dhess - the sqlite3 Connection.execute() method doesn't appear
# to set its cursor's lastrowid, so use an explicit cursor object for
# operations that need lastrowid.

def registrant_rowid(reg, con):
    """Find a registrant in an sqlite3 database.

    Returns the row ID of the matching registrant, or None if there is
    no match.

    reg - The parsed registrant dictionary.

    con - An sqlite3.Connection object.
    
    """
    # address and description may be null; keep the query simple and
    # check address and description in the results.
    con.row_factory = sqlite3.Row
    rows = con.execute('SELECT id, address, description \
                        FROM registrant WHERE \
                          country=:country AND \
                          senate_id=:senate_id AND \
                          name=:name AND \
                          ppb_country=:ppb_country',
                       reg)
    for row in rows:
        if row['address'] == reg['address'] and \
                row['description'] == reg['description']:
            return row['id']
    return None

    
def insert_registrant(reg, con):
    """Insert a registrant into an sqlite3 database.

    Returns the row ID of the inserted registrant.

    As a side effect, this function also inserts rows into the country
    and org tables.

    reg - The parsed registrant dictionary.

    con - An sqlite3.Connection object.

    """
    cur = con.cursor()
    cur.execute('INSERT INTO country VALUES(?)',
                [reg['country']])
    cur.execute('INSERT INTO country VALUES(?)',
                [reg['ppb_country']])
    cur.execute('INSERT INTO org VALUES(?)',
                [reg['name']])
    cur.execute('INSERT INTO registrant VALUES(NULL, \
                           :address, :description, :country, :senate_id, \
                           :name, :ppb_country)',
                reg)
    return cur.lastrowid


def insert_filing(filing, con):
    """Insert a filing into an sqlite3 database.

    Returns the row ID of the inserted filing.

    filing - The parsed filing dictionary.

    con - An sqlite3.Connection object.

    """
    cur = con.cursor()
    cur.execute('INSERT INTO filing VALUES(\
                       :id, :type, :year, :period, :filing_date, :amount, \
                       :registrant)',
                filing)
    return cur.lastrowid

    
def import_filings(con, parsed_filings):
    """Import parsed filings into an sqlite3 database.

    The sqlite3 database is assumed to have a particular schema; see
    filings.sql.
    
    con - A Connection object for the sqlite3 database.

    parsed_filings - A sequence of parsed filings.

    Returns True.
    
    """
    for f in parsed_filings:
        if 'registrant' in f:
            reg = f['registrant']
            regid = registrant_rowid(reg, con)
            if regid is None:
                regid = insert_registrant(reg, con)
        else:
            regid = None
        filing = f['filing']
        filing['registrant'] = regid
        insert_filing(filing, con)
        # Force commit, subsequent records may depend on this one.
        con.commit()
    return True
