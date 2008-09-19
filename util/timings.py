#!/usr/bin/env python
#
# timings.py - Coarse-grained timing for parsing and importing a Senate
# LD-1/LD-2 document.
#
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

"""Coarse-grained timing for parsing and importing a Senate LD-1/LD-2
document.

"""

import lobbyists
import optparse
import sys
import sqlite3
import time

VERSION = '1.0'

def timed_func(func):
    def timer(*args):
        t1 = time.clock()
        result = func(*args)
        t2 = time.clock()
        return result, t2 - t1
    return timer

def parse_all(doc):
    return [x for x in lobbyists.parse_filings(doc)]

def skip_import_list(record, con):
    return list()

def skip_import(record, con):
    return None

def main(argv=None):
    if argv is None:
        argv = sys.argv
    usage = """%prog [OPTIONS] db doc.xml

Parse a Senate LD-1/LD-2 document, then import it into an sqlite3
database. Print the wall-clock time it takes to perform each action.

A document may be identified either by a URL or a file, so long as
it's a valid Senate LD-1/LD-2 XML document.
"""
    parser = optparse.OptionParser(usage=usage,
                                   version=VERSION)
    parser.add_option('-C', '--commit', action='store_true',
                      help='commit changes to the database (default is ' \
                          'not to commit)')
    parser.add_option('-l', '--skip-import-lobbyists', action='store_true',
                      dest='skip_import_lobbyist',
                      help='stub out the lobbyist import functions to ' \
                          'simulate inifinitely-fast lobbyist importing')
    parser.add_option('-c', '--skip-import-client', action='store_true',
                      dest='skip_import_client',
                      help='stub out the client import functions to ' \
                          'simulate inifinitely-fast client importing')
    parser.add_option('-r', '--skip-import-registrant', action='store_true',
                      dest='skip_import_registrant',
                      help='stub out the registrant import functions to ' \
                          'simulate inifinitely-fast registrant importing')
    (options, args) = parser.parse_args(argv[1:])
    if len(args) != 2:
        parser.error('specify one sqlite3 database and one XML document')
    dbname = args[0]
    doc = args[1]
    if options.skip_import_lobbyist:
        lobbyists.entity_importers['lobbyists'] = skip_import_list
    if options.skip_import_client:
        lobbyists.entity_importers['client'] = skip_import
    if options.skip_import_registrant:
        lobbyists.entity_importers['registrant'] = skip_import
    timed_parser = timed_func(parse_all)
    timed_importer = timed_func(lobbyists.import_filings)
    con = sqlite3.connect(dbname)
    filings, parse_time = timed_parser(doc)
    print 'Parse time:', parse_time
    _, import_time = timed_importer(con, filings)
    print 'Import time:', import_time
    if options.commit:
        con.commit()
    con.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
