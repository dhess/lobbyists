# -*- coding: utf-8 -*-
#
# test_import_lobbyists.py - Test lobbyist importing.
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

"""Test lobbyist importing."""

import unittest
import lobbyists
import sqlite3
import util


class TestImportLobbyists(unittest.TestCase):
    def test_import_lobbyists(self):
        """Lobbyist importing."""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

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
        """Lobbyists are matched up with filings in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_lobbyists")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '771F3B6A-315D-4190-88F3-2CE0F138B2B8')
        self.failUnlessEqual(row['lobbyist'], 16)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '771F3B6A-315D-4190-88F3-2CE0F138B2B8')
        self.failUnlessEqual(row['lobbyist'], 15)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist'], 14)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist'], 13)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist'], 12)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BD894C51-AA23-46AE-9802-006B8C91702B')
        self.failUnlessEqual(row['lobbyist'], 11)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '2164D6BB-EBBA-40D2-9C18-16A2D670030A')
        self.failUnlessEqual(row['lobbyist'], 10)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '87A30FA6-7C35-4294-BA43-4CE7B5B808B3')
        self.failUnlessEqual(row['lobbyist'], 9)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist'], 8)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist'], 7)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '0FC23296-F948-43FD-98D4-0912F6579E6A')
        self.failUnlessEqual(row['lobbyist'], 6)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist'], 5)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist'], 4)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist'], 3)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '02DDA99B-725A-4DBA-8397-34892A6918D7')
        self.failUnlessEqual(row['lobbyist'], 2)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '04926911-8A12-4A0E-9DA4-510869446EAC')
        self.failUnlessEqual(row['lobbyist'], 1)

    def test_import_lobbyist_person(self):
        """Importing lobbyists should fill the 'person' table."""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

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
        con = lobbyists.create_db(con)
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
        con = lobbyists.create_db(con)
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
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists_dup.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT lobbyist FROM filing_lobbyists')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_identical_lobbyists2(self):
        """Identical lobbyists shouldn't be duplicated in the database (case 2)."""
        # This test file contains a single filing with two
        # lobbyists. The two lobbyists are exactly the same. This
        # should result in only a single entry in the filing_lobbyists
        # table.
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists_dup2.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT lobbyist FROM filing_lobbyists')
        rows = cur.fetchall()
        self.failUnlessEqual(len(rows), 1)

    def test_import_similar_lobbyists(self):
        """Slightly different lobbyists are inserted into different rows."""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyists_slightly_different.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM lobbyist')
        lobbyers = util.flatten([x['lobbyists'] for x in filings if 'lobbyists' in x])
        self.failUnlessEqual(len(cur.fetchall()), len(lobbyers))


if __name__ == '__main__':
    unittest.main()
