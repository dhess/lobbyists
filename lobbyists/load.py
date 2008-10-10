#!/usr/bin/env python
#
# load.py - Load Senate LD-1/LD-2 XML documents into a database.
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

"""Load Senate LD-1/LD-2 XML documents into a database."""

import lobbyists

def load_db(con, doc):
    """Load all filing records in a lobbyist document into a database.

    Parses and imports filing records from a Senate LD-1/LD-2 XML
    document into a database. Records are parsed and imported one at a
    time.

    con - A DB API 2.0-compliant database Connection object. The
    database must use a compatible schema, e.g., the schema used by
    the create_db function.

    doc - The Senate LD-1/LD-2 XML document to load.

    This function has the side-effects of modifying the connection
    object and populating the database.
    
    Returns the connection object.
    
    """
    lobbyists.import_filings(con.cursor(), lobbyists.parse_filings(doc))
    return con


# Can be run as a script. Note: argv[0] should be the program name.

def main(argv):
    import optparse
    import sqlite3
    
    usage = """%prog [OPTIONS] db doc.xml ...

Parse one or more Senate LD-1/LD-2 XML documents and load them into an
sqlite3 database.

A document may be identified either by a URL or a file, so long as
it's a valid Senate LD-1/LD-2 XML document."""
    parser = optparse.OptionParser(usage=usage,
                                   version=lobbyists.VERSION)
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
        print 'Loading', doc
        con = load_db(con, doc)
        if options.commit:
            con.commit()
    if not options.commit:
        con.commit()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
