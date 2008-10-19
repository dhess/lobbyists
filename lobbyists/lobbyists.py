#
# lobbyists.py - Parse and import U.S. Senate LD-1/LD-2 XML documents.
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

"""Parse and import U.S. Senate LD-1/LD-2 XML documents."""

import xml.dom.pulldom


VERSION = '0.9'


# Attribute parsers.

def _identity(x):
    return x


def _optional(x):
    if x is None:
        return 'unspecified'
    else:
        return x


def _amount(x):
    if x is None:
        return x
    else:
        return int(x)


def _period(x):
    periods = {'1st Quarter (Jan 1 - Mar 31)': 'Q1',
               '2nd Quarter (Apr 1 - June 30)': 'Q2',
               '3rd Quarter (July 1 - Sep 30)': 'Q3',
               '4th Quarter (Oct 1 - Dec 31)': 'Q4',
               'Mid-Year (Jan 1 - Jun 30)': 'H1',
               'Year-End (July 1 - Dec 31)': 'H2',
               'UNDETERMINED': 'undetermined'}
    return periods[x]


def _is_gov(x):
    values = {None: 'unspecified', '0': 'n', '1': 'y'}
    return values[x]


def _status(x):
    status = {0: 'active',
              1: 'terminated',
              2: 'administratively terminated',
              3: 'undetermined'}
    return status[int(x)]


def _lobbyist_indicator(x):
    indicator = {0: 'not covered',
                 1: 'covered',
                 2: 'undetermined'}
    return indicator[int(x)]


# xml.dom.pulldom-specific code

def _filing_elements(doc):
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


def _child_elements(elt):
    """Yield a sequence of child elements of the given DOM element."""
    for child in elt.childNodes:
        if child.nodeType == xml.dom.Node.ELEMENT_NODE:
            yield child


def _attr_of(elt, attrname):
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


def _element_name(elt):
    """The name of the given element."""
    return elt.tagName


# Parsers for DOM elements and their child elements.

def _parse_attrs(elt, attrs):
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
        yield (id, parse(_attr_of(elt, name)))


def _parse_element(elt, id, attrs):
    return (id, dict(_parse_attrs(elt, attrs)))


def _parse_list(list_elt, id, subelt_parser):
    lst = list()
    for subelt in _child_elements(list_elt):
        lst.append(dict([subelt_parser(subelt)]))
    return (id, lst)


_client_attrs = [('ClientCountry', 'country', _optional),
                 ('ClientID', 'senate_id', int),
                 ('ClientName', 'name', _identity),
                 ('ClientPPBCountry', 'ppb_country', _identity),
                 ('ClientPPBState', 'ppb_state', _optional),
                 ('ClientState', 'state', _optional),
                 ('ClientStatus', 'status', _status),
                 ('ContactFullname', 'contact_name', _optional),
                 ('GeneralDescription', 'description', _optional),
                 ('IsStateOrLocalGov', 'state_or_local_gov', _is_gov)]


def _parse_client(elt):
    """Parse a Client DOM element.

    elt - The Client DOM element.

    Returns a pair whose first item is the string 'client' and whose
    second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'client', _client_attrs)


_registrant_attrs = [('Address', 'address', _optional),
                     ('GeneralDescription', 'description', _optional),
                     ('RegistrantCountry', 'country', _identity),
                     ('RegistrantID', 'senate_id', int),
                     ('RegistrantName', 'name', _identity),
                     ('RegistrantPPBCountry', 'ppb_country', _identity)]


def _parse_registrant(elt):
    """Parse a Registrant DOM element.

    elt - The Registrant DOM element.

    Returns a pair whose first item is the string 'registrant' and
    whose second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'registrant', _registrant_attrs)


# LobbyistName uses the '_optional' parser. This is intentional; there
# are a handful of records in the XML documents (see 2008_3_7.xml)
# where the attribute's value is the empty string "".

_lobbyist_attrs = [('LobbyistName', 'name', _optional),
                   ('LobbyistStatus', 'status', _status),
                   ('LobbyisteIndicator', 'indicator', _lobbyist_indicator),
                   ('OfficialPosition', 'official_position', _optional)]


def _parse_lobbyist(elt):
    """Parse a Lobbyist DOM element.

    elt - The Lobbyist DOM element.

    Returns a pair whose first item is the string 'lobbyist' and whose
    second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'lobbyist', _lobbyist_attrs)


def _parse_lobbyists(elt):
    """Parse a Lobbyists DOM element.

    elt - The Lobbyists DOM element.

    Returns a pair whose first item is the string 'lobbyists' and
    whose second item is a list of parsed Lobbyist DOM elements, one
    for each Lobbyist sub-element of this Lobbyists element.

    """
    return _parse_list(elt, 'lobbyists', _parse_lobbyist)


_govt_entity_attrs = [('GovEntityName', 'name', _identity)]


def _parse_govt_entity(elt):
    """Parse a GovernmentEntity DOM element.

    elt - The GovernmentEntity DOM element.

    Returns a pair whose first item is the string 'govt_entity' and
    whose second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'govt_entity', _govt_entity_attrs)


def _parse_govt_entities(elt):
    """Parse a GovernmentEntities DOM element.

    elt - The GovernmentEntities DOM element.

    Returns a pair whose first item is the string 'govt_entities' and
    whose second item is a list of parsed GovernmentEntity DOM
    elements, one for each GovernmentEntity sub-element of this
    GovernmentEntities element.

    """
    return _parse_list(elt, 'govt_entities', _parse_govt_entity)


_issue_attrs = [('Code', 'code', _identity),
                ('SpecificIssue', 'specific_issue', _optional)]


def _parse_issue(elt):
    """Parse an Issue DOM element.

    elt - The Issue DOM element.

    Returns a pair whose first item is the string 'issue' and whose
    second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'issue', _issue_attrs)


def _parse_issues(elt):
    """Parse an Issues DOM element.

    elt - The Issues DOM element.

    Returns a pair whose first item is the string 'issues' and whose
    second item is a list of parsed Issue DOM elements, one for each
    Issue sub-element of this Issues element.

    """
    return _parse_list(elt, 'issues', _parse_issue)


_foreign_entity_attrs = [('ForeignEntityContribution', 'contribution', _amount),
                         ('ForeignEntityCountry', 'country', _optional),
                         ('ForeignEntityName', 'name', _identity),
                         ('ForeignEntityOwnershipPercentage',
                              'ownership_percentage', _amount),
                         ('ForeignEntityPPBcountry', 'ppb_country', _optional),
                         ('ForeignEntityStatus', 'status', _status)]


def _parse_foreign_entity(elt):
    """Parse a (foreign) Entity DOM element.

    elt - The (foreign) Entity DOM element.

    Returns a pair whose first item is the string 'foreign_entity' and
    whose second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'foreign_entity', _foreign_entity_attrs)


def _parse_foreign_entities(elt):
    """Parse a ForeignEntities DOM element.

    elt - The ForeignEntities DOM element.

    Returns a pair whose first item is the string 'foreign_entities'
    and whose second item is a list of parsed (foreign) Entity DOM
    elements, one for each Entity sub-element of this ForeignEntities
    element.

    """
    return _parse_list(elt, 'foreign_entities', _parse_foreign_entity)


# The affiliated org PPB country attribute name is spelled,
# "AffiliatedOrgPPBCcountry" (sic).

_org_attrs = [('AffiliatedOrgCountry', 'country', _optional),
              ('AffiliatedOrgName', 'name', _identity),
              ('AffiliatedOrgPPBCcountry', 'ppb_country', _identity)]


def _parse_org(elt):
    """Parse an Org DOM element.

    elt - The Org DOM element.

    Returns a pair whose first item is the string 'org' and whose
    second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'org', _org_attrs)


def _parse_affiliated_orgs(elt):
    """Parse an AffiliatedOrgs DOM element.

    elt - The AffiliatedOrgs DOM element.

    Returns a pair whose first item is the string 'affiliated_orgs'
    and whose second item is a list of parsed Org DOM elements, one
    for each Org sub-element of this AffiliatedOrgs element.

    """
    return _parse_list(elt, 'affiliated_orgs', _parse_org)


# AffiliatedOrgsURL parser ideally would be a URL parser, but
# unfortunately this element contains all kinds of non-URL junk, and
# must be treated as free-form text.

_filing_attrs = [('ID', 'id', _identity),
                 ('Year', 'year', int),
                 ('Received', 'filing_date', _identity),
                 ('Amount', 'amount', _amount),
                 ('Type', 'type', _identity),
                 ('Period', 'period', _period),
                 ('AffiliatedOrgsURL', 'affiliated_orgs_url', _optional)]


def _parse_filing(elt):
    """Parse a Filing DOM element.

    elt - The Filing DOM element.

    Returns a pair whose first item is the string 'filing' and whose
    second item is the dictionary of parsed attributes.

    """
    return _parse_element(elt, 'filing', _filing_attrs)


# These parsers are used by parse_filings to parse sub-elements of
# Filing DOM elements. The parser is applied to a single argument, the
# DOM element to parse. The parser must return a key-value pair
# ('thing_name': thing_value), which will be inserted into the
# dictionary representing the parsed Filing element.

_subelt_parsers = {'Registrant': _parse_registrant,
                   'Client': _parse_client,
                   'Lobbyists': _parse_lobbyists,
                   'GovernmentEntities': _parse_govt_entities,
                   'Issues': _parse_issues,
                   'ForeignEntities': _parse_foreign_entities,
                   'AffiliatedOrgs': _parse_affiliated_orgs}


def parse_filings(doc):
    """Parse all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    for filing_elt in _filing_elements(doc):
        filing = dict([_parse_filing(filing_elt)])
        for elt in _child_elements(filing_elt):
            parser = _subelt_parsers[_element_name(elt)]
            filing.update([parser(elt)])
        yield filing


# Code to import parsed records into the database.

_where_stmt = {'client':
                   'client WHERE '
                   'country=:country AND '
                   'name=:name AND '
                   'ppb_country=:ppb_country AND '
                   'state=:state AND '
                   'ppb_state=:ppb_state AND '
                   'state_or_local_gov=:state_or_local_gov',
               'registrant':
                   'registrant WHERE '
                   'country=:country AND '
                   'senate_id=:senate_id AND '
                   'name=:name AND '
                   'ppb_country=:ppb_country',
               'lobbyist':
                   'lobbyist WHERE '
                   'name=:name AND '
                   'indicator=:indicator AND '
                   'official_position=:official_position',
               'affiliated_org':
                   'affiliated_org WHERE '
                   'name=:name AND '
                   'country=:country AND '
                   'ppb_country=:ppb_country',
               'foreign_entity':
                   'foreign_entity WHERE '
                   'name=:name AND '
                   'country=:country AND '
                   'ppb_country=:ppb_country'}


def _filing_db_key(filing):
    """Return a filing's database key."""
    return filing['id']


def _rowid(table, tomatch, cur):
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
    stmt = 'SELECT id FROM %s' % _where_stmt[table]
    cur.execute(stmt, tomatch)
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None


def _client_rowid(client, cur):
    """Find a client the database.

    Returns the row ID of the matching client, or None if there is no
    match.

    client - The parsed client dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return _rowid('client', client, cur)


def _import_client(client, filing, cur):
    """Import a client into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'client', 'country',
    'state', 'org' and 'filing_client' tables.

    client - The parsed client dictionary.

    filing - The parsed filing dictionary with which the client is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = _client_rowid(client, cur)
    if db_key is None:
        # Note - client status is pre-inserted into client_status table.
        for key in ['country', 'ppb_country']:
            cur.execute('INSERT INTO country VALUES(?)', [client[key]])
        for key in ['state', 'ppb_state']:
            cur.execute('INSERT INTO state VALUES(?)', [client[key]])
        cur.execute('INSERT INTO person VALUES(?)', [client['contact_name']])
        cur.execute('INSERT INTO org VALUES(?)', [client['name']])
        cur.execute('INSERT INTO client VALUES(NULL, '
                    ':country, :name, :ppb_country, :state, :ppb_state, '
                    ':state_or_local_gov)',
                    client)
        db_key = cur.lastrowid
    cur.execute('INSERT INTO filing_client VALUES(?, ?, ?, ?, ?, ?)',
                [_filing_db_key(filing),
                 db_key,
                 client['senate_id'],
                 client['status'],
                 client['contact_name'],
                 client['description']])


def _registrant_rowid(reg, cur):
    """Find a registrant in the database.

    Returns the row ID of the matching registrant, or None if there is
    no match.

    reg - The parsed registrant dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return _rowid('registrant', reg, cur)


def _import_registrant(reg, filing, cur):
    """Import a registrant into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'registrant', 'country',
    'org' and 'filing_registrant' tables.

    reg - The parsed registrant dictionary.

    filing - The parsed filing dictionary with which the registrant is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = _registrant_rowid(reg, cur)
    if db_key is None:
        cur.execute('INSERT INTO country VALUES(?)',
                    [reg['country']])
        cur.execute('INSERT INTO country VALUES(?)',
                    [reg['ppb_country']])
        cur.execute('INSERT INTO org VALUES(?)',
                    [reg['name']])
        cur.execute('INSERT INTO registrant VALUES(NULL, '
                    ':country, :senate_id, :name, :ppb_country)',
                    reg)
        db_key = cur.lastrowid
    cur.execute('INSERT INTO filing_registrant VALUES(?, ?, ?, ?)',
                [_filing_db_key(filing),
                 db_key,
                 reg['address'],
                 reg['description']])


def _lobbyist_rowid(lobbyist, cur):
    """Find a lobbyist in the database.

    Returns the row ID of the matching lobbyist, or None if there is
    no match.

    lobbyist - The parsed lobbyist dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return _rowid('lobbyist', lobbyist, cur)


def _import_lobbyist(lobbyist, filing, cur):
    """Import a lobbyist into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'lobbyist', 'person' and
    'filing_lobbyists' tables.

    lobbyist - The parsed lobbyist dictionary.

    filing - The parsed filing dictionary with which the lobbyist is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = _lobbyist_rowid(lobbyist, cur)
    if db_key is None:
        # Note - lobbyist status and indicator are pre-inserted into the
        # lobbyist_status and lobbyist_indicator tables.
        cur.execute('INSERT INTO person VALUES(?)', [lobbyist['name']])
        cur.execute('INSERT INTO lobbyist VALUES(NULL, '
                    ':name, :indicator, :official_position)',
                    lobbyist)
        db_key = cur.lastrowid
    cur.execute('INSERT INTO filing_lobbyists VALUES(?, ?, ?)',
                [_filing_db_key(filing), db_key, lobbyist['status']])


def _import_govt_entity(entity, filing, cur):
    """Import a government entity into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'govt_entity' and
    'filing_govt_entities' tables.

    entity - The parsed government entity dictionary.

    filing - The parsed filing dictionary with which the government
    entity is associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = entity['name']
    cur.execute('INSERT INTO govt_entity VALUES(:name)', entity)
    cur.execute('INSERT INTO filing_govt_entities VALUES(?, ?)',
                [_filing_db_key(filing), db_key])


def _import_issue(issue, filing, cur):
    """Import an issue into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'issue', 'issue_code' and
    'filing_issues' tables.

    issue - The parsed issue dictionary.

    filing - The parsed filing dictionary with which the issue is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    cur.execute('INSERT INTO issue_code VALUES(?)', [issue['code']])
    cur.execute('INSERT INTO issue VALUES(NULL, :code, :specific_issue)',
                issue)
    db_key = cur.lastrowid
    cur.execute('INSERT INTO filing_issues VALUES(?, ?)',
                [_filing_db_key(filing), db_key])


def _affiliated_org_rowid(org, cur):
    """Find an affiliated org the database.

    Returns the row ID of the matching org, or None if there is no
    match.

    org - The parsed org dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return _rowid('affiliated_org', org, cur)


def _import_affiliated_org(org, filing, cur):
    """Import an affiliated org into the database.

    Returns nothing.
    
    Side-effects: may insert rows into the 'affiliated_org',
    'country', 'org', 'filing_affiliated_orgs', and 'url' tables.

    org - The parsed org dictionary.

    filing - The parsed filing dictionary with which the org is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = _affiliated_org_rowid(org, cur)
    if db_key is None:
        for key in ['country', 'ppb_country']:
            cur.execute('INSERT INTO country VALUES(?)', [org[key]])
        cur.execute('INSERT INTO org VALUES(?)', [org['name']])
        cur.execute('INSERT INTO affiliated_org VALUES(NULL, '
                    ':name, :country, :ppb_country)',
                    org)
        db_key = cur.lastrowid
    url = filing['affiliated_orgs_url']
    cur.execute('INSERT INTO url VALUES(?)', [url])
    cur.execute('INSERT INTO filing_affiliated_orgs VALUES(?, ?, ?)',
                [_filing_db_key(filing), db_key, url])


def _foreign_entity_rowid(entity, cur):
    """Find a foreign entity in the database.

    Returns the row ID of the matching entity, or None if there is no
    match.

    entity - The parsed foreign entity dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    return _rowid('foreign_entity', entity, cur)


def _import_foreign_entity(entity, filing, cur):
    """Import a foreign entity into the database.

    Returns nothing.

    Side-effects: may insert rows into the 'foreign_entity',
    'country', 'org' and 'filing_foreign_entities' tables.

    entity - The parsed foreign entity dictionary.

    filing - The parsed filing dictionary with which the foreign
    entity is associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    db_key = _foreign_entity_rowid(entity, cur)
    if db_key is None:
        for key in ['country', 'ppb_country']:
            cur.execute('INSERT INTO country VALUES(?)', [entity[key]])
        cur.execute('INSERT INTO org VALUES(?)', [entity['name']])
        cur.execute('INSERT INTO foreign_entity VALUES(NULL, '
                    ':name, :country, :ppb_country)',
                    entity)
        db_key = cur.lastrowid
    cur.execute('INSERT INTO filing_foreign_entities VALUES(?, ?, ?, ?, ?)',
                [_filing_db_key(filing),
                 db_key,
                 entity['contribution'],
                 entity['ownership_percentage'],
                 entity['status']])
                 

def _import_filing(filing, cur):
    """Import a filing into the database.

    Returns nothing.

    Side-effects: inserts a row into the 'filing' table.
    
    filing - The parsed filing dictionary.

    cur - The DB API 2.0-compliant database cursor.

    """
    # The affiliated orgs URL is a special case. It's associated with
    # each affiliated org in the record, so it's handled by the
    # affiliated org importer, and we skip it here.
    cur.execute('INSERT INTO filing VALUES('
                ':id, :type, :year, :period, :filing_date, :amount)',
                filing)


_list_importers = {'lobbyist': _import_lobbyist,
                   'govt_entity': _import_govt_entity,
                   'issue': _import_issue,
                   'org': _import_affiliated_org,
                   'foreign_entity': _import_foreign_entity}


def _import_list(entities, filing, cur):
    """Import a list of parsed entities into the database.

    Returns nothing.

    Side-effects: inserts rows into the database.
    
    entitites - The list of parsed entities.

    filing - The parsed filing dictionary with which the list is
    associated.

    cur - The DB API 2.0-compliant database cursor.

    """
    def entity_id(entities):
        # What kind of list is this? lobbyists? issues? etc.
        return entities[0].keys()[0]
    id = entity_id(entities)
    importer = _list_importers[id]
    for entity in entities:
        importer(entity[id], filing, cur)


# Doesn't include an importer for 'filing'; that one is special.

_entity_importers = [('registrant', _import_registrant),
                     ('client', _import_client),
                     ('lobbyists', _import_list),
                     ('govt_entities', _import_list),
                     ('issues', _import_list),
                     ('affiliated_orgs', _import_list),
                     ('foreign_entities', _import_list)]


def import_filings(cur, parsed_filings):
    """Import parsed filings into the database.

    The database is assumed to have a particular schema; the create_db
    function can be used to create the database.

    cur - The DB API 2.0-compliant database cursor.

    parsed_filings - A sequence of parsed filings.

    Returns the cursor.

    """
    for record in parsed_filings:
        filing = record['filing']
        _import_filing(filing, cur)
        for entity_name, entity_importer in _entity_importers:
            if entity_name in record:
                entity_importer(record[entity_name], filing, cur)
    return cur


def create_db(con):
    """Create the lobbying database.

    con - A DB API 2.0-compliant database Connection object. The
    database will be created via this connection. Note that if the
    connection is made to an existing database, all of the tables in
    that database will be dropped by this function (i.e., the data
    will be lost).

    This function is only guaranteed to work with an sqlite3
    Connection object, but it may work with other SQL databases, as
    well.

    This function has the side-effect of modifying the connection
    object.

    Returns the connection object.

    """
    try:
        # if packaged as a setuptools egg.
        from pkg_resources import resource_string
        script = resource_string(__name__, 'lobbyists.sql')
    except:
        import os.path
        f = open(os.path.join(os.path.dirname(__file__), 'lobbyists.sql'))
        script = ''.join(f.readlines())
    con.executescript(script)
    return con
