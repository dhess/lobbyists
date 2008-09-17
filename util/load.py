#!/usr/bin/env python
#
# load.py - Parse a Senate LD-1/LD-2 document and load it into an
# sqlite3 database.
# Copyright (C) 2008 by Drew Hess <dhess@bothan.net>
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

"""Parse one or more Senate LD-1/LD-2 documents and load them into an
sqlite3 database.

"""

import lobbyists
import optparse
import sys
import sqlite3

VERSION = '1.0'

def main(argv=None):
    if argv is None:
        argv = sys.argv
    usage = """%prog [OPTIONS] db doc.xml ...

Parse one or more Senate LD-1/LD-2 documents and load them into an
sqlite3 database.

A document may be identified either by a URL or a file, so long as
it's a valid Senate LD-1/LD-2 XML document.
"""
    parser = optparse.OptionParser(usage=usage,
                                   version=VERSION)
    parser.add_option('-c', '--commit-per-document', action='store_true',
                      dest='commit',
                      help='commit changes to the database after importing ' \
                           'each document (default is to commit only after all ' \
                           'documents are imported)')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) < 2:
        parser.error('specify exactly one sqlite3 database and at least one ' \
                         'XML document')
    dbname = args[0]
    con = sqlite3.connect(dbname)
    for doc in args[1:]:
        print 'Importing', doc
        lobbyists.import_filings(con, lobbyists.parse_filings(doc))
        if options.commit:
            con.commit()
    if not options.commit:
        con.commit()
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
