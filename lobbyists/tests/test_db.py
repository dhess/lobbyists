# -*- coding: utf-8 -*-
#
# test_db.py - Tests for various database functionality.
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

"""Tests for various database functionality."""

import unittest
import lobbyists
import sqlite3
import util

class TestDB(unittest.TestCase):
    def test_preloaded_table_state_or_local_gov(self):
        """Is the state_or_local_gov table preloaded by the schema file?"""
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
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
        con = lobbyists.create_db(con)
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
        con = lobbyists.create_db(con)
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
        con = lobbyists.create_db(con)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM lobbyist_indicator")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('covered' in rows)
        self.failUnless('not covered' in rows)
        self.failUnless('undetermined' in rows)


if __name__ == '__main__':
    unittest.main()
