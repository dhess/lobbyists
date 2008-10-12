# -*- coding: utf-8 -*-
#
# test_import_registrants.py - Test registrant importing.
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

"""Test registrant importing."""

import unittest
import lobbyists
import sqlite3
import util

class TestImportRegistrants(unittest.TestCase):
    def test_import_registrant_countries(self):
        """Importing registrants fills the 'country' table."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM country")
        rows = [row['name'] for row in cur]
        registrants = [x for x in filings if 'registrant' in x]
        countries = set([x['registrant']['country'] for x in registrants])
        countries = countries.union([x['registrant']['ppb_country'] for x in \
                                         registrants])
        self.failUnlessEqual(len(rows), len(countries))
        for country in countries:
            self.failUnless(country in rows)
        
    def test_import_registrant_orgs(self):
        """Importing registrants fills the 'org' table."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM org")
        rows = [row['name'] for row in cur]
        registrants = [x for x in filings if 'registrant' in x]
        orgs = set([x['registrant']['name'] for x in registrants])
        self.failUnlessEqual(len(rows), len(orgs))
        for org in orgs:
            self.failUnless(org in rows)
        
    def test_import_identical_registrants(self):
        """Identical registrants shouldn't be duplicated in the database"""
        filings = list(lobbyists.parse_filings(util.testpath('registrants_dup.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_registrants(self):
        """Slightly different registrants are inserted into different rows."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants_slightly_different.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        self.failUnlessEqual(len(cur.fetchall()), len(filings))


if __name__ == '__main__':
    unittest.main()
