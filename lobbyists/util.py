#!/usr/bin/env python
#
# util.py - Utility functions for the lobbyists package.
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

"""Utility functions for the lobbyists package."""

import lobbyists
import sqlite3
import os.path

def load_db(docs, dbname, clobber=False, commit_per_doc=False):
    """Load filing records from lobbyist documents into an sqlite3 database.

    Parses and imports filing records from one or more Senate
    LD-1/LD-2 XML documents into an sqlite3 database. Records are
    parsed and imported one at a time.

    docs - A sequence of URLs or filenames identifying the LD-1/LD-2
    XML documents load load.
    
    dbname - The filename of the sqlite3 database to load. If the
    database doesn't exist, load_db creates it.
    
    clobber - If True, and the database already exists, the database's
    contents will be clobbered prior to loading.

    commit_per_doc - If True, load_db will commit the changes to the
    database after loading each individual document. If False (the
    default), load_db only commits when the last document is
    loaded. Per-document committing ensures that successfully loaded
    documents are committed to the database in case of parsing or
    importing errors in subsequent documents, but is slower.
    
    This function has the side-effect of creating and/or modifying the
    database.
    
    Returns the database's sqlite3.Connection object.
    
    """
    create_db = clobber or not os.path.exists(dbname)
    con = sqlite3.connect(dbname)
    if create_db:
        lobbyists.create_db(con)
    for doc in docs:
        lobbyists.import_filings(con.cursor(), lobbyists.parse_filings(doc))
        if commit_per_doc:
            con.commit()
    if not commit_per_doc:
        con.commit()
    return con


def load_main(argv=None):
    """Run the lobbyists-load script directly from Python.

    Note that argv[0] is the program name.

    """
    import optparse
    import sys
    import sqlite3

    if argv is None:
        argv = sys.argv
    usage = """%prog [OPTIONS] db doc.xml ...

Parse one or more Senate LD-1/LD-2 XML documents and load them into an
sqlite3 database.

Each document may be identified either by a URL or a file, so long as
it's a valid Senate LD-1/LD-2 XML document.

If db doesn't exist, %prog will create it prior to loading the first
document."""
    parser = optparse.OptionParser(usage=usage,
                                   version=lobbyists.VERSION)
    parser.add_option('-C', '--clobber-database', action='store_true',
                      dest='clobber',
                      help='clobber the existing database contents prior to ' \
                          'loading first document')
    parser.add_option('-c', '--commit-per-document', action='store_true',
                      dest='commit',
                      help='commit changes to the database after importing ' \
                          'each document (default is to commit only after all ' \
                          'documents are imported)')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) < 2:
        parser.error('specify exactly one sqlite3 database and at least one ' \
                         'XML document')
    con = load_db(args[1:], args[0], options.clobber, options.commit)
    con.close()
    return 0
