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
        filings = [x for x in lobbyists.parse_filings(util.testpath('filings.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        # Read back, sort and compare
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing")
        rows = [row for row in cur]
        rows.sort(key=lambda x: x['id'])
        filings.sort(key=lambda x: x['filing']['id'])

        self.failUnlessEqual(len(rows), len(filings))
        for (row, filing) in zip(rows, lobbyists.filing_values(filings)):
            self.failUnlessEqual(row['id'], filing['id'])
            self.failUnlessEqual(row['type'], filing['type'])
            self.failUnlessEqual(row['year'], filing['year'])
            self.failUnlessEqual(row['period'], filing['period'])
            self.failUnlessEqual(row['filing_date'], filing['filing_date'])
            self.failUnlessEqual(row['amount'], filing['amount'])
            # All of these filings have no Registrant.
            self.failUnless(row['registrant'] is None)
        
    def test_import_filings_to_registrants(self):
        """Ensure filing rows point to the correct registrants."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT filing.id AS filing_id, \
                            registrant.address AS address, \
                            registrant.description AS description, \
                            registrant.country AS country, \
                            registrant.senate_id AS senate_id, \
                            registrant.name AS name, \
                            registrant.ppb_country AS ppb_country \
                     FROM filing INNER JOIN registrant ON \
                            registrant.id=filing.registrant")
        rows = [row for row in cur]
        rows.sort(key=lambda x: x['filing_id'])
        registrants = [x for x in filings if 'registrant' in x]
        registrants.sort(key=lambda x: x['filing']['id'])
        self.failUnlessEqual(len(rows), len(registrants))
        for (row, filing) in zip(rows, registrants):
            self.failUnlessEqual(row['filing_id'], filing['filing']['id'])
            reg = filing['registrant']
            self.failUnlessEqual(row['address'], reg['address'])
            self.failUnlessEqual(row['description'], reg['description'])
            self.failUnlessEqual(row['country'], reg['country'])
            self.failUnlessEqual(row['senate_id'], reg['senate_id'])
            self.failUnlessEqual(row['name'], reg['name'])
            self.failUnlessEqual(row['ppb_country'], reg['ppb_country'])

    # Multiple filings with the exact same registrant info should
    # share the same registrant row ID in the database; i.e., there
    # should not be duplicate registrant rows in the database.
    #
    # Registrant address and description are optional. When they're
    # not included in a particular registrant record, they're
    # represented as NULL in the database. Because of the details of
    # the importing implementation, there are 4 tests for identical
    # registrant records, one for each combination of missing/present
    # address and description.
            
    def test_import_identical_registrants1(self):
        """Identical registrants shouldn't be duplicated in the database (case 1)."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_dup1.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])


    def test_import_identical_registrants2(self):
        """Identical registrants shouldn't be duplicated in the database (case 2)."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_dup2.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])


    def test_import_identical_registrants3(self):
        """Identical registrants shouldn't be duplicated in the database (case 3)."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_dup3.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])


    def test_import_identical_registrants4(self):
        """Identical registrants shouldn't be duplicated in the database (case 4)."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_dup4.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_registrants(self):
        """Ensure slightly different registrants are inserted into different rows."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_slightly_different.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        self.failUnlessEqual(len(cur.fetchall()), len(filings))

        
if __name__ == '__main__':
    unittest.main()
