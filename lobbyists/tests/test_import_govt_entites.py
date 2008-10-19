# -*- coding: utf-8 -*-
#
# test_import_govt_entities.py - Test govt entity importing.
# Copyright (C) 2008 by Drew Hess <dhess@bothan.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Test govt entity importing."""

import unittest
import lobbyists
import sqlite3
import util


class TestImportGovtEntities(unittest.TestCase):
    def test_import_govt_entities(self):
        """Government entity importing."""
        filings = list(lobbyists.parse_filings(util.testpath('govt_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM govt_entity")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['name'],
                             'Federal Communications Commission (FCC)')

        row = rows.pop()
        self.failUnlessEqual(row['name'],
                             'Environmental Protection Agency (EPA)')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Energy, Dept of')

        row = rows.pop()
        self.failUnlessEqual(row['name'],
                             'Federal Energy Regulatory Commission (FERC)')

        row = rows.pop()
        self.failUnlessEqual(row['name'],
                             'Health & Human Services, Dept of  (HHS)')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'SENATE')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'HOUSE OF REPRESENTATIVES')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'NONE')

        self.failUnlessEqual(len(rows), 0)

    def test_import_filings_to_govt_entities(self):
        """Government entities are matched up with filings in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('govt_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_govt_entities")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '2627E811-33AB-43F4-B8E0-5B979A10FBF9')
        self.failUnlessEqual(row['govt_entity'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'],
                             'Federal Communications Commission (FCC)')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'],
                             'Environmental Protection Agency (EPA)')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'],'Energy, Dept of')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'],
                             'HOUSE OF REPRESENTATIVES')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'],
                             'Federal Energy Regulatory Commission (FERC)')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        self.failUnlessEqual(row['govt_entity'], 'SENATE')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'],
                             'Health & Human Services, Dept of  (HHS)')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'], 'SENATE')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        self.failUnlessEqual(row['govt_entity'],
                             'HOUSE OF REPRESENTATIVES')

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'FD29F4AF-763B-42A6-A27E-0AE115CD6D51')
        self.failUnlessEqual(row['govt_entity'], 'NONE')

        self.failUnlessEqual(len(rows), 0)


if __name__ == '__main__':
    unittest.main()
