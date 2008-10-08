#!/usr/bin/env python
#
# catalog.py - build a catalog of values in an LD-1/LD-2 database.
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

"""Build a catalog of values in an LD-1/LD-2 database.

Supported fields:

filing type
filing period
filing "augmented type" (type + amount and period).

"""

import lobbyists
import optparse
import sys
import pprint

VERSION = '1.0'

def filing_type(x):
    return x['filing']['type']

def filing_amount(x):
    return x['filing']['amount']

def filing_period(x):
    return x['filing']['period']

def catalog(doc, f):
    return set(f(x) for x in lobbyists.parse_filings(doc))


def catalog_types(doc):
    """Returns the set of all filing types encountered in doc.

    doc - The document to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of filing types (represented as strings) found in
    doc.

    """
    return catalog(doc, filing_type)
            

def catalog_augmented_types(doc):
    """Returns the set of all "augmented" filing types encountered in doc.

    The augmented type is a combination of the type, period and amount
    fields of a filing record.
    
    The presence or absence of an amount field in a filing record is
    considered part of its augmented type. For example, if two filing
    records have the type 'year-end report', but one has a reported
    amount and the other doesn't, the records are treated as having
    different types. Records with a reported amount equal to 0 are
    considered yet another separate type.

    Records with an "undetermined" period are also counted as a
    separate augmented type.

    doc - The document to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of augmented types (represented as strings) found
    in doc.

    """
    def augmented_type(x):
        basic_type = filing_type(x)
        if filing_period(x) == 'undetermined':
            basic_type += ' (undetermined period)'
        amount = filing_amount(x)
        if amount is None:
            return basic_type
        elif amount == 0:
            return basic_type + ' (w/ zero amount)'
        else:
            return basic_type + ' (w/ amount)'
    return catalog(doc, augmented_type)


def catalog_periods(doc):
    """Returns the set of all filing periods encountered in doc.

    doc - The document to parse. Can be a filename, a URL or anything
    else that xml.dom.pulldom.parse takes as an argument.

    Returns the set of period names (represented as strings) found in
    doc.

    """
    return catalog(doc, filing_period)
    

def main(argv=None):
    if argv is None:
        argv = sys.argv
    usage = """%prog [OPTIONS] field db.xml ...

Print to stdout a catalog of values in a Senate lobbyists document.

Multiple documents may be specified. A document may be either a URL or
a file, so long as it's a valid Senate lobbyist XML document.

Currently supported fields are:

  type           - Filing type (year-end report, registration, etc.).
  period         - Filing period (1st quarter, mid-year, etc.).
  augmented_type - Filing type plus amount and period."""
    parser = optparse.OptionParser(usage=usage,
                                   version=VERSION)
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
        parer.error('unknown or unsupported field name "%s"' % args[0])
    s = set()
    for doc in args[1:]:
        s = s.union(catalog_fun(doc))
    for x in sorted(s):
        print x
    return 0


if __name__ == "__main__":
    sys.exit(main())
