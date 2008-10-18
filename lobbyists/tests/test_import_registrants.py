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
    def test_import_registrants(self):
        """Import registrants."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT filing_registrant.filing AS filing_id, \
                            filing_registrant.address AS address, \
                            filing_registrant.description AS description, \
                            registrant.country AS country, \
                            registrant.senate_id AS senate_id, \
                            registrant.name AS name, \
                            registrant.ppb_country AS ppb_country \
                     FROM filing_registrant INNER JOIN registrant ON \
                            registrant.id=filing_registrant.registrant")
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
        cur.execute('SELECT filing_registrant.registrant \
                      FROM filing_registrant')
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
        cur.execute('SELECT * FROM registrant')
        self.failUnlessEqual(len(cur.fetchall()), len(filings))

    def test_import_registrant_different_description(self):
        """Registrants with different description but otherwise identical should occupy same row."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants_different_description.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM registrant")
        rows = [row for row in cur]
        self.failUnlessEqual(len(rows), 1)
        
    def test_import_registrant_different_address(self):
        """Registrants with different address but otherwise identical should occupy same row."""
        filings = list(lobbyists.parse_filings(util.testpath('registrants_different_address.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM registrant")
        rows = [row for row in cur]
        self.failUnlessEqual(len(rows), 1)
        

if __name__ == '__main__':
    unittest.main()
