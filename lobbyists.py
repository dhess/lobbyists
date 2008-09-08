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

def optional(x):
    if x is None:
        return 'unspecified'
    else:
        return x
        
def amount(x):
    if x is None:
        return x
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

def is_gov(x):
    values = { None: 'missing', '0': 'n', '1': 'y'}
    return values[x]

def client_status(x):
    # Senate web page that provides the key for the client status code
    # lists '3: undetermined', but in practice this value doesn't
    # occur in any of the XML documents.
    status = {
        0: 'active',
        1: 'terminated',
        2: 'administratively terminated'
        }
    return status[int(x)]


# xml.dom.pulldom-specific code
    
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


def attr_of(elt, attrname):
    """Get the value of an attribute of an element.

    Returns the value of an attribute of the specified DOM element, or
    None if no such attribute exists in the element.
    
    elt - The DOM element.

    attrname - The name of the attribute to retrieve.

    """
    val = elt.getAttribute(attrname)
    if val == '':
        return None
    else:
        return val
    

def element_name(elt):
    """The name of the given element."""
    return elt.tagName


# Parsers for DOM elements and their child elements.
    
def parse_attrs(elt, attrs):
    """Parse the attributes of a DOM element into a sequence of pairs.

    elt - The DOM element.

    attrs - A sequence of tuples of 3 items each. The first item is
    the attribute name (a string). The second is the identifier
    associated with the parsed attribute value in the yielded
    pair. The third is the parsing function. It's applied to the
    attribute's DOM value, and its output is stored with the
    identifier in the yielded pair.

    Note that the value of an attribute which doesn't appear in the
    element is None.

    Yields a sequence of (identifier, value) pairs.

    """
    for name, id, parse in attrs:
        yield (id, parse(attr_of(elt, name)))


def parse_element(elt, id, attrs):
    # Caller expects a sequence
    return [(id, dict(parse_attrs(elt, attrs)))]


client_attrs = [('ClientCountry', 'country', identity),
                ('ClientID', 'senate_id', int),
                ('ClientName', 'name', identity),
                ('ClientPPBCountry', 'ppb_country', identity),
                ('ClientPPBState', 'ppb_state', identity),
                ('ClientState', 'state', identity),
                ('ClientStatus', 'status', client_status),
                ('ContactFullname', 'contact_name', identity),
                ('GeneralDescription', 'description', identity),
                ('IsStateOrLocalGov', 'state_or_local_gov', is_gov)]

def parse_client(elt):
    """Parse a Client DOM element.

    elt - The Client DOM element.

    Returns a list with one item, a pair whose first item is the
    string 'client' and whose second item is the dictionary of parsed
    attributes.
    
    """
    return parse_element(elt, 'client', client_attrs)

    
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


subelt_parsers = {
    'Registrant': parse_registrant,
    'Client': parse_client
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


# Code to import parsed records into the database.
        
# XXX dhess - the sqlite3 Connection.execute() method doesn't appear
# to set its cursor's lastrowid, so use an explicit cursor object for
# operations that need lastrowid.

def client_rowid(client, con):
    """Find a client in an sqlite3 database.

    Returns the row ID of the matching client, or None if there is no
    match.

    client - The parsed client dictionary.

    con - An sqlite3.Connection object.

    """
    # ppb_state, state and description may be null; keep the query
    # simple and check these fields in the results.
    con.row_factory = sqlite3.Row
    rows = con.execute('SELECT id, state, ppb_state, description \
                        FROM client WHERE \
                          country=:country AND \
                          senate_id=:senate_id AND \
                          name=:name AND \
                          ppb_country=:ppb_country AND \
                          status=:status AND \
                          state_or_local_gov=:state_or_local_gov AND \
                          contact_name=:contact_name',
                       client)
    for row in rows:
        if row['ppb_state'] == client['ppb_state'] and \
                row['state'] == client['state'] and \
                row['description'] == client['description']:
            return row['id']
    return None


def insert_client(client, con):
    """Insert a client into an sqlite3 database.

    Returns the row ID of the inserted client.

    As a side effect, this function also inserts rows into the
    'country', 'state' and 'org' tables.

    client - The parsed client dictionary.

    con - An sqlite3.Connection object.

    """
    cur = con.cursor()
    # Note - client status is pre-inserted into DB.
    for key in ['country', 'ppb_country']:
        cur.execute('INSERT INTO country VALUES(?)', [client[key]])
    for key in ['state', 'ppb_state']:
        # May be null
        val = client[key]
        if val:
            cur.execute('INSERT INTO state VALUES(?)', [val])
    cur.execute('INSERT INTO org VALUES(?)', [client['name']])
    cur.execute('INSERT INTO client VALUES(NULL, \
                   :country, :senate_id, :name, :ppb_country, \
                   :state, :ppb_state, :status, :description, \
                   :state_or_local_gov, :contact_name)',
                client)
    return cur.lastrowid


def registrant_rowid(reg, con):
    """Find a registrant in an sqlite3 database.

    Returns the row ID of the matching registrant, or None if there is
    no match.

    reg - The parsed registrant dictionary.

    con - An sqlite3.Connection object.
    
    """
    cur = con.cursor()
    cur.execute('SELECT id \
                 FROM registrant WHERE \
                      address=:address AND \
                      description=:description AND \
                      country=:country AND \
                      senate_id=:senate_id AND \
                      name=:name AND \
                      ppb_country=:ppb_country',
                reg)
    row = cur.fetchone()
    if row:
        return row[0]
    else:
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
                       :registrant, :client)',
                filing)
    return cur.lastrowid


def import_entity(record, con, name, findrow, insert):
    if name in record:
        entity = record[name]
        rowid = findrow(entity, con)
        if rowid is None:
            return insert(entity, con)
        else:
            return rowid
    else:
        return None

    
def import_registrant(record, con):
    return import_entity(record,
                         con,
                         'registrant',
                         registrant_rowid,
                         insert_registrant)


def import_client(record, con):
    return import_entity(record,
                         con,
                         'client',
                         client_rowid,
                         insert_client)


entity_importers = {
    'registrant': import_registrant,
    'client': import_client,
    }

def import_filings(con, parsed_filings):
    """Import parsed filings into an sqlite3 database.

    The sqlite3 database is assumed to have a particular schema; see
    filings.sql.
    
    con - A Connection object for the sqlite3 database.

    parsed_filings - A sequence of parsed filings.

    Returns True.
    
    """
    for record in parsed_filings:
        filing = record['filing']
        for entity_name, entity_importer in entity_importers.items():
            filing[entity_name] = entity_importer(record, con)
        insert_filing(filing, con)
        # Force commit, subsequent records may depend on this one.
        con.commit()
    return True
