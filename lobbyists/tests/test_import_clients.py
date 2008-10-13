# -*- coding: utf-8 -*-
#
# test_import_clients.py - Test client importing.
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

"""Test client importing."""

import unittest
import lobbyists
import sqlite3
import util

class TestImportClients(unittest.TestCase):
    def test_import_identical_clients(self):
        """Identical clients shouldn't be duplicated in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('clients_dup.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT client FROM filing')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_clients(self):
        """Slightly different clients are inserted into different rows."""
        filings = list(lobbyists.parse_filings(util.testpath('clients_slightly_different.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM client')
        clients = [x['client'] for x in filings if 'client' in x]
        self.failUnlessEqual(len(cur.fetchall()), len(clients))

    def test_import_client_orgs(self):
        """Importing clients should fill the 'org' table."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM org")
        rows = [row['name'] for row in cur]
        clients = [x for x in filings if 'client' in x]
        orgs = set([x['client']['name'] for x in clients])
        self.failUnlessEqual(len(rows), len(orgs))
        for org in orgs:
            self.failUnless(org in rows)

    def test_import_client_countries(self):
        """Importing clients should fill the 'country' table."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM country")
        rows = [row['name'] for row in cur]
        clients = [x for x in filings if 'client' in x]
        countries = set([x['client']['country'] for x in clients])
        countries = countries.union([x['client']['ppb_country'] for x in \
                                         clients])
        self.failUnlessEqual(len(rows), len(countries))
        for country in countries:
            self.failUnless(country in rows)


    def test_import_client_states(self):
        """Importing clients should fill the 'state' table."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM state")
        rows = [row['name'] for row in cur]
        clients = [x for x in filings if 'client' in x]
        states = set([x['client']['state'] for x in clients])
        states = states.union([x['client']['ppb_state'] for x in \
                                   clients])
        self.failUnlessEqual(len(rows), len(states))
        for state in states:
            self.failUnless(state in rows)

    def test_import_client_persons(self):
        """Importing clients should fill the 'person' table."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM person")
        rows = [row['name'] for row in cur]
        clients = [x for x in filings if 'client' in x]
        persons = set([x['client']['contact_name'] for x in clients])
        self.failUnlessEqual(len(rows), len(persons))
        for person in persons:
            self.failUnless(person in rows)

    def test_import_client_state_or_local_gov(self):
        """After importing clients, state_or_local_gov table should be unchanged (it's pre-loaded)."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT val FROM state_or_local_gov")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('unspecified' in rows)
        self.failUnless('y' in rows)
        self.failUnless('n' in rows)

    def test_import_client_client_status(self):
        """After importing clients, client_status table should be unchanged (it's pre-loaded)."""
        filings = list(lobbyists.parse_filings(util.testpath('clients.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM client_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('administratively terminated' in rows)


if __name__ == '__main__':
    unittest.main()
