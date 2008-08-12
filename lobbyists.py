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

def amount(x):
    if x == '':
        return x
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
    

filing_attrs = {
    'ID': ('id', identity),
    'Year': ('year', int),
    'Received': ('filing_date', identity),
    'Amount': ('amount', amount),
    'Type': ('type', identity),
    'Period': ('period', period)
    }

def parse_filings(doc):
    """Iterate over all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a sequence of dictionaries, one per filing record.

    """
    dom = xml.dom.pulldom.parse(doc)
    for event, node in dom:
        if event == 'START_ELEMENT' and node.nodeName == 'Filing':
            filing = {}
            for attr, (id, parse) in filing_attrs.items():
                filing[id] = parse(node.getAttribute(attr))
            yield filing


normalize_exceptions = {
    'amount': -1
    }

def normalize(record, default='unspecified', exceptions=normalize_exceptions):
    """Normalize a record.

    Records in the LD-1/LD-2 database are frequently missing
    information. For example, a quarterly report might not specify
    which individual lobbyists participated in lobbying activity
    during that quarter. Missing fields in these records are
    represented by the parse_* functions as keys whose values are
    the empty string ('').

    For each key in a record whose value is '', this function replaces
    that value with a more meaningful value; e.g., replace the
    key-value pair 'amount': '' with 'amount': -1.
    
    record - The record to normalize (a dictionary).

    default - The default normalized value.

    exceptions - A mapping of special keys and their normalized
    values. If a key whose value in the record is unspecified is found
    in this mapping, use the coresponding value rather than the
    default normalized value.

    """
    def norm((k, v)):
        if v == '':
            if k in exceptions:
                return k, exceptions[k]
            else:
                return k, default
        return k, v
    return dict(map(norm, record.items()))
