#!/usr/bin/env python
#
# catalog.py - catalog attribute values in an LD-1/LD-2 database.
# Copyright (C) 2008 by Drew Hess <dhess@bothan.net>.
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

"""Catalog attribute values in an LD-1/LD-2 database.

Supported attribute types:

Filing Type
Filing Period
Filing "augmented type" (type + amount and period).

"""

import xml.dom.pulldom
import optparse
import sys
import pprint

VERSION = '1.0'

def filing_records(doc):
    """Iterate over all filing records in a lobbyist database.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Yields a 'Filing' xml.dom.Node instance. Note that the nodes are
    not expanded.
    """
    dom = xml.dom.pulldom.parse(doc)
    for event, node in dom:
        if event == 'START_ELEMENT' and node.nodeName == 'Filing':
            yield node


def catalog_types(doc):
    """Returns the set of all filing types encountered in doc.

    Identifies all filing records in doc, creates a catalog of their
    types and returns the catalog (as a set).

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of type names (represented as strings) found in
    doc.

    """
    return set(n.getAttribute('Type') for n in filing_records(doc))
            

def catalog_augmented_types(doc):
    """Returns the set of all "augmented" filing types encountered in doc.

    Identifies all filing records in doc, creates a catalog of their
    "augmented" types and returns the catalog (as a set).

    The augmented type is a combination of the Type, Period and Amount
    attributes of a Filing element.
    
    The presence or absence of an Amount attribute in a filing record
    is considered part of its augmented type. For example, if two
    filing records have the Type 'year-end report', but one has an
    Amount attribute and the other doesn't, the records are treated as
    different types.

    Note that, with one exception, the value of the Amount attribute
    is not considered part of the augmented type, only the presence or
    absence of the attribute itself. For example, two records with the
    same Type value, one with an Amount of 10000 and the other with an
    Amount of 5000, are treated as the same augmented type. The single
    exception is the value 0; records with a 0 amount are treated as
    yet another augmented type.

    Records with an "undeterimined" Period attribute are also counted
    as a separate augmented type.

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of augmented type names (represented as strings)
    found in doc.
    """
    def augmented_type(n):
        basic_type = n.getAttribute('Type')
        if n.getAttribute('Period').lower() == "undetermined":
            basic_type += ' (undetermined period)'
        amount = n.getAttribute('Amount')  # '' if no such attribute
        if amount == '':
            return basic_type
        elif amount == '0':
            return basic_type + ' (w/ zero amount)'
        else:
            return basic_type + ' (w/ amount)'
    return set(augmented_type(n) for n in filing_records(doc))


def catalog_periods(doc):
    """Returns the set of all filing periods encountered in doc.

    Identifies all filing records in doc, creates a catalog of their
    periods and returns the catalog (as a set).

    doc - The database to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of period names (represented as strings) found in
    doc.

    """
    return set(n.getAttribute('Period') for n in filing_records(doc))
    

def main(argv=None):
    if argv is None:
        argv = sys.argv
    usage = """%prog [OPTIONS] attr db.xml ...

Print to stdout a catalog of all attributes of a particular type in a
Senate lobbyists database.

Multiple databases can be given, and a database may be either a URL or
a file, so long as it's a valid Senate lobbyist XML document.

Currently supported attributes are:

  type           - Filing type (year-end report, registration, etc.).
  period         - Filing period (1st quarter, mid-year, etc.).
  augmented_type - Filing type plus amount and period."""
    parser = optparse.OptionParser(usage=usage,
                                   version=VERSION)
    parser.add_option('-a', '--with-amounts', action='store_true',
                      dest='amounts',
                      help='if a record has an amount attribute, count it as a separate record type')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) < 2:
        parser.error('specify exactly one type and at least one XML document')
    if args[0] == 'type':
        catalog_fun = catalog_types
    elif args[0] == 'augmented_type':
        catalog_fun = catalog_augmented_types
    elif args[0] == 'period':
        catalog_fun = catalog_periods
    else:
        parer.error('unknown or unsupported attribute type "%s"' % args[0])
    s = set()
    for doc in args[1:]:
        s = s.union(catalog_fun(doc))
    for x in sorted(s):
        print x
    return 0


if __name__ == "__main__":
    sys.exit(main())
