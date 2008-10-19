# -*- coding: utf-8 -*-
#
# test_import_foreign_entities.py - Test foreign entity importing.
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

"""Test foreign entity importing."""

import unittest
import lobbyists
import sqlite3
import util


class TestImportForeignEntities(unittest.TestCase):
    def test_import_foreign_entities(self):
        """Import foreign entities"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM foreign_entity")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['id'], 16)
        self.failUnlessEqual(row['name'], 'THE NEWS CORPORATION LTD.')
        self.failUnlessEqual(row['country'], 'UNDETERMINED')
        self.failUnlessEqual(row['ppb_country'], 'AUSTRALIA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 15)
        self.failUnlessEqual(row['name'], 'EMBASSY OF VENEZUELA')
        self.failUnlessEqual(row['country'], 'UNDETERMINED')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 14)
        self.failUnlessEqual(row['name'], 'Japan Tobacco Inc.')
        self.failUnlessEqual(row['country'], 'JAPAN')
        self.failUnlessEqual(row['ppb_country'], 'JAPAN')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 13)
        self.failUnlessEqual(row['name'], 'N/A')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 12)
        self.failUnlessEqual(row['name'], 'N/A')
        self.failUnlessEqual(row['country'], 'UNDETERMINED')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 11)
        self.failUnlessEqual(row['name'], 'WALLETTE, GERALD')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 10)
        self.failUnlessEqual(row['name'], 'CITIZENS FOR DEMOCRACTIC RULE IN NIGERIA')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 9)
        self.failUnlessEqual(row['name'], 'CITIZENS FOR DEMOCRACTIC RULE IN NIGERIA')
        self.failUnlessEqual(row['country'], 'UNDETERMINED')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 8)
        self.failUnlessEqual(row['name'], 'Beta Gamma Ltd.')
        self.failUnlessEqual(row['country'], 'SEYCHELLES')
        self.failUnlessEqual(row['ppb_country'], 'SEYCHELLES')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 7)
        self.failUnlessEqual(row['name'], "FBC Group Ltd.")
        self.failUnlessEqual(row['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(row['ppb_country'], 'UNITED KINGDOM')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 6)
        self.failUnlessEqual(row['name'], 'AgustaWestland Holdings, Ltd.')
        self.failUnlessEqual(row['country'], '<SELECT ONE>')
        self.failUnlessEqual(row['ppb_country'], '<SELECT ONE>')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 5)
        self.failUnlessEqual(row['name'], 'HITACHI, LTD.')
        self.failUnlessEqual(row['country'], 'unspecified')
        self.failUnlessEqual(row['ppb_country'], 'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 4)
        self.failUnlessEqual(row['name'], 'EVONIK INDUSTRIES GMBH')
        self.failUnlessEqual(row['country'], 'GERMANY')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 3)
        self.failUnlessEqual(row['name'], 'MARUHA CORP')
        self.failUnlessEqual(row['country'], 'JAPAN')
        self.failUnlessEqual(row['ppb_country'], 'JAPAN')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 2)
        self.failUnlessEqual(row['name'], 'HOKO FISHING CO')
        self.failUnlessEqual(row['country'], 'JAPAN')
        self.failUnlessEqual(row['ppb_country'], 'JAPAN')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 1)
        self.failUnlessEqual(row['name'], 'NORTH JAPAN MARITIME CORP')
        self.failUnlessEqual(row['country'], 'JAPAN')
        self.failUnlessEqual(row['ppb_country'], 'JAPAN')

        self.failUnlessEqual(len(rows), 0)

    def test_import_filing_to_foreign_entities(self):
        """Foreign entities are matched up with filings in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_foreign_entities")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'E4382341-0E5D-4A31-8A7D-3CCB71E8EF6E')
        self.failUnlessEqual(row['contribution'], 0)
        self.failUnlessEqual(row['ownership_percentage'], 34)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 16)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'EEDBB5F5-8BB4-4E0D-9F10-CD8FDD2A0D70')
        self.failUnlessEqual(row['contribution'], 100000)
        self.failUnlessEqual(row['ownership_percentage'], 0)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 15)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BBF87FC8-73FC-4050-B6F8-850C79EC72E2')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], 100)
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['foreign_entity'], 14)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'CE714D21-6713-4764-87F2-5F6294F0FBB3')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 13)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'CE714D21-6713-4764-87F2-5F6294F0FBB3')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'terminated')
        self.failUnlessEqual(row['foreign_entity'], 12)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BECA0C94-4308-47E5-BF23-887D3954E254')
        self.failUnlessEqual(row['contribution'], 0)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 11)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BECA0C94-4308-47E5-BF23-887D3954E254')
        self.failUnlessEqual(row['contribution'], 0)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 10)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'BECA0C94-4308-47E5-BF23-887D3954E254')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 9)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        self.failUnlessEqual(row['contribution'], 300000)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['foreign_entity'], 8)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        self.failUnlessEqual(row['contribution'], 300000)
        self.failUnlessEqual(row['ownership_percentage'], 100)
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['foreign_entity'], 7)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '63AC4585-74BC-478D-A356-FCCFD98FDE64')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], 100)
        self.failUnlessEqual(row['status'], 'active')
        self.failUnlessEqual(row['foreign_entity'], 6)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '498EAE8A-DE7A-4FFF-A813-062D92FDA271')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], 100)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 5)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'ACD87507-EB78-4607-95E8-43871D9D1EF2')
        self.failUnlessEqual(row['contribution'], None)
        self.failUnlessEqual(row['ownership_percentage'], 100)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 4)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A9F81F8B-F0B0-440A-8564-051FF553CCA8')
        self.failUnlessEqual(row['contribution'], 0)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 3)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A9F81F8B-F0B0-440A-8564-051FF553CCA8')
        self.failUnlessEqual(row['contribution'], 16500)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 2)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A9F81F8B-F0B0-440A-8564-051FF553CCA8')
        self.failUnlessEqual(row['contribution'], 16500)
        self.failUnlessEqual(row['ownership_percentage'], None)
        self.failUnlessEqual(row['status'], 'undetermined')
        self.failUnlessEqual(row['foreign_entity'], 1)

        self.failUnlessEqual(len(rows), 0)

    def test_import_foreign_entities_org(self):
        """Importing foreign entities should fill the 'org' table."""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM org")
        rows = [row for row in cur]
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'THE NEWS CORPORATION LTD.')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'EMBASSY OF VENEZUELA')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Japan Tobacco Inc.')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'N/A')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'WALLETTE, GERALD')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'CITIZENS FOR DEMOCRACTIC RULE IN NIGERIA')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Beta Gamma Ltd.')
        row = rows.pop()
        self.failUnlessEqual(row['name'], "FBC Group Ltd.")
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'AgustaWestland Holdings, Ltd.')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'HITACHI, LTD.')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'EVONIK INDUSTRIES GMBH')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'MARUHA CORP')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'HOKO FISHING CO')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'NORTH JAPAN MARITIME CORP')
        self.failUnlessEqual(len(rows), 0)

    def test_import_foreign_entities_country(self):
        """Importing foreign entities should fill the 'country' table."""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM country")
        rows = [row for row in cur]
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'AUSTRALIA')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UNDETERMINED')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'SEYCHELLES')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UNITED KINGDOM')
        row = rows.pop()
        self.failUnlessEqual(row['name'], '<SELECT ONE>')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'unspecified')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'USA')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'GERMANY')
        row = rows.pop()
        self.failUnlessEqual(row['name'], 'JAPAN')
        self.failUnlessEqual(len(rows), 0)

    def test_import_foreign_entity_foreign_entity_status(self):
        """After import, foreign_entity_status table should be unchanged (it's pre-loaded)."""
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT status FROM foreign_entity_status")
        rows = set([row[0] for row in cur])
        self.failUnlessEqual(len(rows), 3)
        self.failUnless('active' in rows)
        self.failUnless('terminated' in rows)
        self.failUnless('undetermined' in rows)

    def test_import_identical_foreign_entities(self):
        """Identical foreign entitites shouldn't be duplicated in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities_dup.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT foreign_entity from filing_foreign_entities')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_foreign_entities(self):
        """Slightly different foreign_entities are inserted into different rows."""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities_slightly_different.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM foreign_entity')
        orgs = util.flatten([x['foreign_entities'] for x in filings if 'foreign_entities' in x])
        self.failUnlessEqual(len(cur.fetchall()), len(orgs))

    def test_import_foreign_entity_different_status(self):
        """Foreign entities with different status but otherwise identical should occupy same row"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities_different_status.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM foreign_entity")
        rows = [row for row in cur]
        self.failUnlessEqual(len(rows), 1)

    def test_import_foreign_entity_different_contribution(self):
        """Foreign entities with different contribution but otherwise identical should occupy same row"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities_different_contribution.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM foreign_entity")
        rows = [row for row in cur]
        self.failUnlessEqual(len(rows), 1)

    def test_import_foreign_entity_different_ownership(self):
        """Foreign entities with different percentage ownership but otherwise identical should occupy same row"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entities_different_ownership.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM foreign_entity")
        rows = [row for row in cur]
        self.failUnlessEqual(len(rows), 1)

        

if __name__ == '__main__':
    unittest.main()
