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
    def test_preloaded_table_state_or_local_gov(self):
        """Is the state_or_local_gov table preloaded by the schema file?"""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT val FROM state_or_local_gov")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('unspecified' in rows)
        self.failUnless('y' in rows)
        self.failUnless('n' in rows)
        
    def test_preloaded_table_client_status(self):
        """Is the client_status table preloaded by the schema file?"""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM client_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('administratively terminated' in rows)
        
    def test_preloaded_table_lobbyist_status(self):
        """Is the lobbyist_status table preloaded by the schema file?"""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM lobbyist_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('undetermined' in rows)
        
    def test_preloaded_table_lobbyist_indicator(self):
        """Is the lobbyist_indicator table preloaded by the schema file?"""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM lobbyist_indicator")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('covered' in rows)
        self.failUnless('not covered' in rows)
        self.failUnless('undetermined' in rows)
        
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

    def test_import_registrant_countries(self):
        """Ensure importing registrants fills the 'country' table."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

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
        """Ensure importing registrants fills the 'org' table."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrants.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM org")
        rows = [row['name'] for row in cur]
        registrants = [x for x in filings if 'registrant' in x]
        orgs = set([x['registrant']['name'] for x in registrants])
        self.failUnlessEqual(len(rows), len(orgs))
        for org in orgs:
            self.failUnless(org in rows)
        
    def dup_test(self, file, column, table):
        filings = [x for x in lobbyists.parse_filings(util.testpath(file))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT %s FROM %s' % (column, table))
        row1, row2 = cur.fetchall()
        return row1, row2

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
        row1, row2 = self.dup_test('clients_dup.xml', 'client', 'filing')
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_clients(self):
        """Ensure slightly different clients are inserted into different rows."""
        filings = [x for x in lobbyists.parse_filings(\
                util.testpath('clients_slightly_different.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM client')
        clients = [x['client'] for x in filings if 'client' in x]
        self.failUnlessEqual(len(cur.fetchall()), len(clients))

    def test_import_client_orgs(self):
        """Importing clients should fill the 'org' table."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
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
        filings = [x for x in lobbyists.parse_filings(util.testpath('clients.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM client_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('administratively terminated' in rows)

    def test_import_lobbyists(self):
        """Check lobbyist importing."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyists.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        # Some of the other import tests just compare the parsed
        # filings to the contents of the database, but for various
        # reasons that's difficult for lobbyist records.  Instead,
        # this test has knowledge of the contents of the
        # 'lobbyists.xml' test file, and checks the database contents
        # explicitly, ala the parser tests in test_parser.py.
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM lobbyist")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['id'], 16)
        self.failUnlessEqual(row['name'], 'KNUTSON, KENT')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'undetermined')
        self.failUnlessEqual(row['official_position'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 15)
        self.failUnlessEqual(row['name'], 'KNUTSON, KENT')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 14)
        self.failUnlessEqual(row['name'], 'CHAMPLIN, STEVEN')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'ExecFlrAsst, H. Maj. Whip; ExecDir, H.DemCauc.')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 13)
        self.failUnlessEqual(row['name'], 'GRIFFIN, BRIAN')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'StaffAsst, DemPolicyComm; FlrAsst, MinoritySec')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 12)
        self.failUnlessEqual(row['name'], 'DUBERSTEIN, KENNETH')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'Chief of Staff, President Reagan')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 11)
        self.failUnlessEqual(row['name'], 'UELAND, ERIC')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'AsstEditor/Ed./Res.Dir, Sen.Rep.PolicyComm;')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 10)
        self.failUnlessEqual(row['name'], 'BEDWELL, EDWARD T')
        self.failUnlessEqual(row['status'], 'terminated')
        self.failUnlessEqual(row['indicator'], 'undetermined')
        self.failUnlessEqual(row['official_position'], 'unspecified')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 9)
        self.failUnlessEqual(row['name'], 'LEHMAN (MY 2006), PATRICK')
        self.failUnlessEqual(row['status'], 'terminated')
        self.failUnlessEqual(row['indicator'], 'undetermined')
        self.failUnlessEqual(row['official_position'], 'unspecified')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 8)
        self.failUnlessEqual(row['name'], 'NEAL, KATIE')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'covered')
        self.failUnlessEqual(row['official_position'], 'COMM DIR/REP DINGELL')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 7)
        self.failUnlessEqual(row['name'], 'NEAL, KATIE')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 6)
        self.failUnlessEqual(row['name'], 'NEAL, KATIE')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'undetermined')
        self.failUnlessEqual(row['official_position'], 'unspecified')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 5)
        self.failUnlessEqual(row['name'], 'unspecified')
        self.failUnlessEqual(row['status'], 'terminated')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'unspecified')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 4)
        self.failUnlessEqual(row['name'], 'MCKENNEY, WILLIAM')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'Staff Director, Ways & Means Over Sub')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 3)
        self.failUnlessEqual(row['name'], 'DENNIS, JAMES')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'Tax Counsel, Sen Robb - Counsel, Sen Bingaman')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 2)
        self.failUnlessEqual(row['name'], 'GRAFMEYER, RICHARD')
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['indicator'], 'not covered')
        self.failUnlessEqual(row['official_position'], 'Deputy Chief of Staff, JCT')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 1)
        self.failUnlessEqual(row['name'], 'HARRIS, ROBERT L.')
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['indicator'], 'undetermined')
        self.failUnlessEqual(row['official_position'], 'unspecified')
        
        self.failUnlessEqual(len(rows), 0)

    def test_import_filings_to_lobbyists(self):
        """Ensure lobbyists are matched up with filings in the database."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyists.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_lobbyists")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '771F3B6A-315D-4190-88F3-2CE0F138B2B8')
        self.failUnlessEqual(row['lobbyist_id'], 16)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '771F3B6A-315D-4190-88F3-2CE0F138B2B8')
        self.failUnlessEqual(row['lobbyist_id'], 15)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist_id'], 14)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist_id'], 13)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist_id'], 12)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist_id'], 11)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '2164D6BB-EBBA-40D2-9C18-16A2D670030A')
        self.failUnlessEqual(row['lobbyist_id'], 10)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '87A30FA6-7C35-4294-BA43-4CE7B5B808B3')
        self.failUnlessEqual(row['lobbyist_id'], 9)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist_id'], 8)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist_id'], 7)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist_id'], 6)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist_id'], 5)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist_id'], 4)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist_id'], 3)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist_id'], 2)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing_id'],
                             '04926911-8A12-4A0E-9DA4-510869446EAC')
        self.failUnlessEqual(row['lobbyist_id'], 1)
        
    def test_import_lobbyist_person(self):
        """Importing lobbyists should fill the 'person' table."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyists.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM person")
        rows = [row['name'] for row in cur]
        lobbyers = util.flatten([x['lobbyists'] for x in filings if 'lobbyists' in x])
        names = set([x['lobbyist']['name'] for x in lobbyers])
        self.failUnlessEqual(len(rows), len(names))
        for name in names:
            self.failUnless(name in rows)

    def test_import_lobbyist_lobbyist_status(self):
        """After import, lobbyist_status table should be unchanged (it's pre-loaded)."""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM lobbyist_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('undetermined' in rows)
        
    def test_import_lobbyist_lobbyist_indicator(self):
        """After import, lobbyist_indicator table should be unchanged (it's pre-loaded)."""
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM lobbyist_indicator")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('covered' in rows)
        self.failUnless('not covered' in rows)
        self.failUnless('undetermined' in rows)
        
    def test_import_identical_lobbyists(self):
        """Identical lobbyists shouldn't be duplicated in the database."""
        row1, row2 = self.dup_test('lobbyists_dup.xml', 'lobbyist_id', 'filing_lobbyists')
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_lobbyists(self):
        """Ensure slightly different lobbyists are inserted into different rows."""
        filings = [x for x in lobbyists.parse_filings(\
                util.testpath('lobbyists_slightly_different.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM lobbyist')
        lobbyers = util.flatten([x['lobbyists'] for x in filings if 'lobbyists' in x])
        self.failUnlessEqual(len(cur.fetchall()), len(lobbyers))

    def test_import_govt_entities(self):
        """Check government entity importing."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('govt_entities.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM govt_entity")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['id'], 8)
        self.failUnlessEqual(row['name'],
                             'Federal Communications Commission (FCC)')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 7)
        self.failUnlessEqual(row['name'],
                             'Environmental Protection Agency (EPA)')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 6)
        self.failUnlessEqual(row['name'], 'Energy, Dept of')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 5)
        self.failUnlessEqual(row['name'],
                             'Federal Energy Regulatory Commission (FERC)')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 4)
        self.failUnlessEqual(row['name'],
                             'Health & Human Services, Dept of  (HHS)')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 3)
        self.failUnlessEqual(row['name'], 'SENATE')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 2)
        self.failUnlessEqual(row['name'], 'HOUSE OF REPRESENTATIVES')
        
        row = rows.pop()
        self.failUnlessEqual(row['id'], 1)
        self.failUnlessEqual(row['name'], 'NONE')
        
        self.failUnlessEqual(len(rows), 0)

    def test_import_filings_to_govt_entities(self):
        """Ensure government entities are matched up with filings in the database."""
        filings = [x for x in lobbyists.parse_filings(util.testpath('govt_entities.xml'))]
        con = sqlite3.connect(':memory:')
        con.executescript(util.sqlscript('filings.sql'))
        self.failUnless(lobbyists.import_filings(con, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_govt_entities")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 8)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 7)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 6)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 2)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 5)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 3)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'], 4)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'], 3)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'], 2)
        
        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FD29F4AF-763B-42A6-A27E-0AE115CD6D51')
        self.failUnlessEqual(row['govt_entity'], 1)
        
        self.failUnlessEqual(len(rows), 0)
        
if __name__ == '__main__':
    unittest.main()
