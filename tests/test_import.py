# -*- coding: utf-8 -*-
#
# test_import.py - Tests for the lobbyists module import_* functions.
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

"""Tests for the lobbyists module import_* functions."""

import unittest
import lobbyists
import sqlite3
import util

class TestImport(unittest.TestCase):
    def test_import_filings(self):
        filings = [lobbyists.normalize(x) for x in \
                       lobbyists.parse_filings(util.testpath('filings.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        # Read back, sort and compare
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing")
        rows = [row for row in cur]
        rows.sort(key=lambda x: x['id'])
        filings.sort(key=lambda x: x['id'])

        self.failUnlessEqual(len(rows), len(filings))
        for (row, filing) in zip(rows, filings):
            self.failUnlessEqual(row['id'], filing['id'])
            self.failUnlessEqual(row['type'], filing['type'])
            self.failUnlessEqual(row['year'], filing['year'])
            self.failUnlessEqual(row['period'], filing['period'])
            self.failUnlessEqual(row['filing_date'], filing['filing_date'])
            self.failUnlessEqual(row['amount'], filing['amount'])

        
if __name__ == '__main__':
    unittest.main()
