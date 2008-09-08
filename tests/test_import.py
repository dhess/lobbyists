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

def filing_values(parsed_filings):
    """Iterate over filing dictionaries in a sequence of parsed filings."""
    for x in parsed_filings:
        yield x['filing']


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
        for (row, filing) in zip(rows, filing_values(filings)):
            self.failUnlessEqual(row['id'], filing['id'])
            self.failUnlessEqual(row['type'], filing['type'])
            self.failUnlessEqual(row['year'], filing['year'])
            self.failUnlessEqual(row['period'], filing['period'])
            self.failUnlessEqual(row['filing_date'], filing['filing_date'])
            self.failUnlessEqual(row['amount'], filing['amount'])
            # All of these filings have no Registrant, no Client.
            self.failUnless(row['registrant'] is None)
            self.failUnless(row['client'] is None)
        
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

    def dup_test(self, file, column):
        filings = [x for x in lobbyists.parse_filings(util.testpath(file))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.%s FROM filing' % column)
        row1, row2 = cur.fetchall()
        return row1, row2

    def similarity_test(self, file, column):
        filings = [x for x in lobbyists.parse_filings(util.testpath(file))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT filing.registrant \
                      FROM filing')
        return len(cur.fetchall()), len(filings)
        
    def test_import_identical_registrants(self):
        """Identical registrants shouldn't be duplicated in the database"""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants_dup.xml'))]
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

    def test_import_filings_to_clients(self):
        """Ensure filing rows point to the correct clients."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
                  
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT filing.id AS filing_id, \
                            client.country AS country, \
                            client.senate_id as senate_id, \
                            client.name as name, \
                            client.ppb_country as ppb_country, \
                            client.state as state, \
                            client.ppb_state as ppb_state, \
                            client.status as status, \
                            client.description as description, \
                            client.state_or_local_gov as state_or_local_gov, \
                            client.contact_name as contact_name \
                     FROM filing INNER JOIN client ON \
                            client.id=filing.client")
        rows = [row for row in cur]
        rows.sort(key=lambda x: x['filing_id'])
        clients = [x for x in filings if 'client' in x]
        clients.sort(key=lambda x: x['filing']['id'])
        self.failUnlessEqual(len(rows), len(clients))
        for (row, filing) in zip(rows, clients):
            self.failUnlessEqual(row['filing_id'], filing['filing']['id'])
            client = filing['client']
            self.failUnlessEqual(row['country'], client['country'])
            self.failUnlessEqual(row['senate_id'], client['senate_id'])
            self.failUnlessEqual(row['name'], client['name'])
            self.failUnlessEqual(row['ppb_country'], client['ppb_country'])
            self.failUnlessEqual(row['state'], client['state'])
            self.failUnlessEqual(row['ppb_state'], client['ppb_state'])
            self.failUnlessEqual(row['status'], client['status'])
            self.failUnlessEqual(row['description'], client['description'])
            self.failUnlessEqual(row['state_or_local_gov'], client['state_or_local_gov'])
            self.failUnlessEqual(row['contact_name'], client['contact_name'])

    def test_import_identical_clients(self):
        """Identical clients shouldn't be duplicated in the database."""
        row1, row2 = self.dup_test('clients_dup.xml', 'client')
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_registrants(self):
        """Ensure slightly different registrants are inserted into different rows."""
        n1, n2 = self.similarity_test('clients_slightly_different.xml', 'client')
        self.failUnlessEqual(n1, n2)


if __name__ == '__main__':
    unittest.main()
