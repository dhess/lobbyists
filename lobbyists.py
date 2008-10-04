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
    values = { None: 'unspecified', '0': 'n', '1': 'y'}
    return values[x]

def status(x):
    status = {
        0: 'active',
        1: 'terminated',
        2: 'administratively terminated',
        3: 'undetermined'
        }
    return status[int(x)]

def lobbyist_indicator(x):
    indicator = {
        0: 'not covered',
        1: 'covered',
        2: 'undetermined'
        }
    return indicator[int(x)]


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
    return (id, dict(parse_attrs(elt, attrs)))


def parse_list(list_elt, id, subelt_parser):
    lst = list()
    for subelt in child_elements(list_elt):
        lst.append(dict([subelt_parser(subelt)]))
    return (id, lst)
    

client_attrs = [('ClientCountry', 'country', optional),
                ('ClientID', 'senate_id', int),
                ('ClientName', 'name', identity),
                ('ClientPPBCountry', 'ppb_country', identity),
                ('ClientPPBState', 'ppb_state', optional),
                ('ClientState', 'state', optional),
                ('ClientStatus', 'status', status),
                ('ContactFullname', 'contact_name', optional),
                ('GeneralDescription', 'description', optional),
                ('IsStateOrLocalGov', 'state_or_local_gov', is_gov)]

def parse_client(elt):
    """Parse a Client DOM element.

    elt - The Client DOM element.

    Returns a pair whose first item is the string 'client' and whose
    second item is the dictionary of parsed attributes.
    
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

    Returns a pair whose first item is the string 'registrant' and
    whose second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'registrant', registrant_attrs)


# LobbyistName uses the 'optional' parser. This is intentional; there
# are a handful of records in the XML documents (see 2008_3_7.xml)
# where the attribute's value is the empty string "".

lobbyist_attrs = [('LobbyistName', 'name', optional),
                  ('LobbyistStatus', 'status', status),
                  ('LobbyisteIndicator', 'indicator', lobbyist_indicator),
                  ('OfficialPosition', 'official_position', optional)]

def parse_lobbyist(elt):
    """Parse a Lobbyist DOM element.

    elt - The Lobbyist DOM element.

    Returns a pair whose first item is the string 'lobbyist' and whose
    second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'lobbyist', lobbyist_attrs)


def parse_lobbyists(elt):
    """Parse a Lobbyists DOM element.

    elt - The Lobbyists DOM element.

    Returns a pair whose first item is the string 'lobbyists' and
    whose second item is a list of parsed Lobbyist DOM elements, one
    for each Lobbyist sub-element of this Lobbyists element.

    """
    return parse_list(elt, 'lobbyists', parse_lobbyist)


govt_entity_attrs = [('GovEntityName', 'name', identity)]

def parse_govt_entity(elt):
    """Parse a GovernmentEntity DOM element.

    elt - The GovernmentEntity DOM element.

    Returns a pair whose first item is the string 'govt_entity' and
    whose second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'govt_entity', govt_entity_attrs)


def parse_govt_entities(elt):
    """Parse a GovernmentEntities DOM element.

    elt - The GovernmentEntities DOM element.

    Returns a pair whose first item is the string 'govt_entities' and
    whose second item is a list of parsed GovernmentEntity DOM
    elements, one for each GovernmentEntity sub-element of this
    GovernmentEntities element.

    """
    return parse_list(elt, 'govt_entities', parse_govt_entity)


issue_attrs = [('Code', 'code', identity),
               ('SpecificIssue', 'specific_issue', optional)]

def parse_issue(elt):
    """Parse an Issue DOM element.

    elt - The Issue DOM element.

    Returns a pair whose first item is the string 'issue' and whose
    second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'issue', issue_attrs)


def parse_issues(elt):
    """Parse an Issues DOM element.

    elt - The Issues DOM element.

    Returns a pair whose first item is the string 'issues' and whose
    second item is a list of parsed Issue DOM elements, one for each
    Issue sub-element of this Issues element.

    """
    return parse_list(elt, 'issues', parse_issue)


def parse_foreign_entities(elt):
    return ('foreign_entities', list())


# The affiliated org PPB country attribute name is spelled,
# "AffiliatedOrgPPBCcountry" (sic).

org_attrs = [('AffiliatedOrgCountry', 'country', optional),
             ('AffiliatedOrgName', 'name', identity),
             ('AffiliatedOrgPPBCcountry', 'ppb_country', identity)]

def parse_org(elt):
    """Parse an Org DOM element.

    elt - The Org DOM element.

    Returns a pair whose first item is the string 'org' and whose
    second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'org', org_attrs)


def parse_affiliated_orgs(elt):
    """Parse an AffiliatedOrgs DOM element.

    elt - The AffiliatedOrgs DOM element.

    Returns a pair whose first item is the string 'affiliated_orgs'
    and whose second item is a list of parsed Org DOM elements, one
    for each Org sub-element of this AffiliatedOrgs element.

    """
    return parse_list(elt, 'affiliated_orgs', parse_org)


# AffiliatedOrgsURL parser ideally would be a URL parser, but
# unfortunately this element contains all kinds of non-URL junk, and
# must be treated as free-form text.

filing_attrs = [('ID', 'id', identity),
                ('Year', 'year', int),
                ('Received', 'filing_date', identity),
                ('Amount', 'amount', amount),
                ('Type', 'type', identity),
                ('Period', 'period', period),
                ('AffiliatedOrgsURL', 'affiliated_orgs_url', optional)]

def parse_filing(elt):
    """Parse a Filing DOM element.

    elt - The Filing DOM element.

    Returns a pair whose first item is the string 'filing' and whose
    second item is the dictionary of parsed attributes.

    """
    return parse_element(elt, 'filing', filing_attrs)


# These parsers are used by parse_filings to parse sub-elements of
# Filing DOM elements. The parser is applied to a single argument, the
# DOM element to parse. The parser must return a key-value pair
# ('thing_name': thing_value), which will be inserted into the
# dictionary representing the parsed Filing element.

subelt_parsers = {
    'Registrant': parse_registrant,
    'Client': parse_client,
    'Lobbyists': parse_lobbyists,
    'GovernmentEntities': parse_govt_entities,
    'Issues': parse_issues,
    'ForeignEntities': parse_foreign_entities,
    'AffiliatedOrgs': parse_affiliated_orgs
    }

def parse_filings(doc):
    """Parse all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    for filing_elt in filing_elements(doc):
        filing = dict([parse_filing(filing_elt)])
        for elt in child_elements(filing_elt):
            parser = subelt_parsers[element_name(elt)]
            filing.update([parser(elt)])
        yield filing


# Code to import parsed records into the database.
        
where_stmt = {
    'client':
        'client WHERE ' \
        'country=:country AND ' \
        'senate_id=:senate_id AND '\
        'name=:name AND ' \
        'ppb_country=:ppb_country AND ' \
        'state=:state AND ' \
        'ppb_state=:ppb_state AND ' \
        'status=:status AND ' \
        'description=:description AND ' \
        'state_or_local_gov=:state_or_local_gov AND ' \
        'contact_name=:contact_name',
    'registrant':
        'registrant WHERE ' \
        'address=:address AND ' \
        'description=:description AND ' \
        'country=:country AND ' \
        'senate_id=:senate_id AND ' \
        'name=:name AND ' \
        'ppb_country=:ppb_country',
    'lobbyist':
        'lobbyist WHERE ' \
        'name=:name AND ' \
        'status=:status AND ' \
        'indicator=:indicator AND ' \
        'official_position=:official_position'
    }
    
def rowid(table, tomatch, cur):
    """Find a match in a database table and return its rowid.

    This function only works for tables with a primary key
    auto-increment column named 'id'.
    
    table - The name of the table to search (a string).

    tomatch - A mapping whose key names are identical to the table's
    column names, and whose values are the values to match in the
    table.

    cur - The DB API 2.0-compliant database cursor.
    
    Returns the rowid of the matching row, or None if no match is
    found.

    """
    stmt = 'SELECT id FROM %s' % where_stmt[table]
    cur.execute(stmt, tomatch)
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None


def client_rowid(client, cur):
    """Find a client the database.

    Returns the row ID of the matching client, or None if there is no
    match.

    client - The parsed client dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return rowid('client', client, cur)


def insert_client(client, cur):
    """Insert a client into the database.

    Returns the row ID of the inserted client.

    As a side effect, this function also inserts rows into the
    'country', 'state' and 'org' tables.

    client - The parsed client dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    # Note - client status is pre-inserted into client_status table.
    for key in ['country', 'ppb_country']:
        cur.execute('INSERT INTO country VALUES(?)', [client[key]])
    for key in ['state', 'ppb_state']:
        cur.execute('INSERT INTO state VALUES(?)', [client[key]])
    cur.execute('INSERT INTO person VALUES(?)', [client['contact_name']])
    cur.execute('INSERT INTO org VALUES(?)', [client['name']])
    cur.execute('INSERT INTO client VALUES(NULL, \
                   :country, :senate_id, :name, :ppb_country, \
                   :state, :ppb_state, :status, :description, \
                   :state_or_local_gov, :contact_name)',
                client)
    return cur.lastrowid


def registrant_rowid(reg, cur):
    """Find a registrant in the database.

    Returns the row ID of the matching registrant, or None if there is
    no match.

    reg - The parsed registrant dictionary.

    cur - The DB API 2.0-compliant database cursor.
    
    """
    return rowid('registrant', reg, cur)

    
def insert_registrant(reg, cur):
    """Insert a registrant into the database.

    Returns the row ID of the inserted registrant.

    As a side effect, this function also inserts rows into the country
    and org tables.

    reg - The parsed registrant dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
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


def lobbyist_rowid(lobbyist, cur):
    """Find a lobbyist in the database.

    Returns the row ID of the matching lobbyist, or None if there is
    no match.

    lobbyist - The parsed lobbyist dictionary.

    cur - The DB API 2.0-compliant database cursor.
    
    """
    return rowid('lobbyist', lobbyist, cur)


def insert_lobbyist(lobbyist, cur):
    """Insert a lobbyist into the database.

    Returns the row ID of the inserted lobbyist.

    As a side effect, this function also inserts rows into the
    'person' table.

    lobbyist - The parsed lobbyist dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    # Note - lobbyist status and indicator are pre-inserted into the
    # lobbyist_status and lobbyist_indicator tables.
    cur.execute('INSERT INTO person VALUES(?)', [lobbyist['name']])
    cur.execute('INSERT INTO lobbyist VALUES(NULL, \
                   :name, :status, :indicator, :official_position)',
                lobbyist)
    return cur.lastrowid


def insert_govt_entity(entity, cur):
    """Insert a government entity into the database.

    Returns the key (NOT the rowid!) of the inserted entry.

    entity - The parsed government entity dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    cur.execute('INSERT INTO govt_entity VALUES(:name)', entity)
    return entity['name']


def insert_issue(issue, cur):
    """Insert an issue into the database.

    Returns the row ID of the inserted issue.

    As a side effect, this function also inserts rows into the
    'issue_code' table.

    issue - The parsed issue dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    cur.execute('INSERT INTO issue_code VALUES(?)', [issue['code']])
    cur.execute('INSERT INTO issue VALUES(NULL, :code, :specific_issue)',
                issue)
    return cur.lastrowid


def insert_filing(filing, cur):
    """Insert a filing and its relationships into the database.

    Returns the row ID of the inserted filing.

    filing - The parsed filing dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    # Insert the filing first, then its relationships.
    cur.execute('INSERT INTO filing VALUES(\
                       :id, :type, :year, :period, :filing_date, :amount, \
                       :registrant, :client)',
                filing)
    filing_rowid = cur.lastrowid
    for id in filing['lobbyists']:
        cur.execute('INSERT INTO filing_lobbyists VALUES(?, ?)',
                    [filing['id'], id])
    for id in filing['govt_entities']:
        cur.execute('INSERT INTO filing_govt_entities VALUES(?, ?)',
                    [filing['id'], id])
    for id in filing['issues']:
        cur.execute('INSERT INTO filing_issues VALUES(?, ?)',
                    [filing['id'], id])
    return filing_rowid


def import_entity(record, cur, name, findrow, insert):
    if name in record:
        entity = record[name]
        rowid = findrow(entity, cur)
        if rowid is None:
            return insert(entity, cur)
        else:
            return rowid
    else:
        return None


def import_registrant(record, cur):
    return import_entity(record,
                         cur,
                         'registrant',
                         registrant_rowid,
                         insert_registrant)


def import_client(record, cur):
    return import_entity(record,
                         cur,
                         'client',
                         client_rowid,
                         insert_client)


def import_lobbyist(record, cur):
    return import_entity(record,
                         cur,
                         'lobbyist',
                         lobbyist_rowid,
                         insert_lobbyist)


def import_govt_entity(record, cur):
    return insert_govt_entity(record['govt_entity'], cur)


def import_issue(record, cur):
    return insert_issue(record['issue'], cur)


def import_list(record, id, entity_importer, cur):
    ids = list()
    if id in record:
        for entity in record[id]:
            ids.append(entity_importer(entity, cur))
    return ids


def import_lobbyists(record, cur):
    """Returns a list of rowids for the lobbyists in a filing record.

    record - The parsed filing dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return import_list(record, 'lobbyists', import_lobbyist, cur)


def import_govt_entities(record, cur):
    """Returns a list of keys for the govt entities in a filing record.

    record - The parsed filing dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return import_list(record, 'govt_entities', import_govt_entity, cur)


def import_issues(record, cur):
    """Returns a list of rowids for the issues in a filing record.

    record - The parsed filing dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return import_list(record, 'issues', import_issue, cur)


entity_importers = {
    'registrant': import_registrant,
    'client': import_client,
    'lobbyists': import_lobbyists,
    'govt_entities': import_govt_entities,
    'issues': import_issues,
    }

def import_filings(cur, parsed_filings):
    """Import parsed filings into the database.

    The database is assumed to have a particular schema; see
    filings.sql for a schema that can be used with sqlite3.
    
    cur - The DB API 2.0-compliant database cursor.

    parsed_filings - A sequence of parsed filings.

    Returns True.
    
    """
    for record in parsed_filings:
        filing = record['filing']
        for entity_name, entity_importer in entity_importers.items():
            filing[entity_name] = entity_importer(record, cur)
        insert_filing(filing, cur)
    return True
