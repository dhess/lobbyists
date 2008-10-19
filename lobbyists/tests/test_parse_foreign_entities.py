# -*- coding: utf-8 -*-
#
# test_parse_foreign_entities.py - Tests for lobbyists foreign entities parsing.
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

"""Tests for lobbyists foreign entities parsing."""

import unittest
import lobbyists
import util


class TestParseForeignEntities(unittest.TestCase):
    def test_contribution(self):
        """Parse foreign entity contribution"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_contribution.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'ACD87507-EB78-4607-95E8-43871D9D1EF2')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['contribution'], None)
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A9F81F8B-F0B0-440A-8564-051FF553CCA8')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['contribution'], 0)
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['contribution'], 16500)
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['contribution'], 16500)
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_country(self):
        """Parse foreign entity country"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_country.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '63AC4585-74BC-478D-A356-FCCFD98FDE64')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], '<SELECT ONE>')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '498EAE8A-DE7A-4FFF-A813-062D92FDA271')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'unspecified')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'ACD87507-EB78-4607-95E8-43871D9D1EF2')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'GERMANY')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BECA0C94-4308-47E5-BF23-887D3954E254')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'USA')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'USA')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'UNDETERMINED')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'SEYCHELLES')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_name(self):
        """Parse foreign entity name"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_name.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CE714D21-6713-4764-87F2-5F6294F0FBB3')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'], 'N/A')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'], 'N/A')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BECA0C94-4308-47E5-BF23-887D3954E254')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'], 'WALLETTE, GERALD')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'],
                             'CITIZENS FOR DEMOCRACTIC RULE IN NIGERIA')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'],
                             'CITIZENS FOR DEMOCRACTIC RULE IN NIGERIA')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'], 'Beta Gamma Ltd.')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['name'], 'FBC Group Ltd.')
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_ownership_percentage(self):
        """Parse foreign entity ownership percentage"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_ownership_percentage.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ownership_percentage'], None)
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ownership_percentage'], 100)
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E4382341-0E5D-4A31-8A7D-3CCB71E8EF6E')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ownership_percentage'], 34)
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'EEDBB5F5-8BB4-4E0D-9F10-CD8FDD2A0D70')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ownership_percentage'], 0)
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_ppb_country(self):
        """Parse foreign entity PPB country"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_country.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '63AC4585-74BC-478D-A356-FCCFD98FDE64')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], '<SELECT ONE>')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '498EAE8A-DE7A-4FFF-A813-062D92FDA271')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'unspecified')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'ACD87507-EB78-4607-95E8-43871D9D1EF2')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'USA')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BECA0C94-4308-47E5-BF23-887D3954E254')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'USA')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'USA')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'UNDETERMINED')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '4CAC3894-FA4C-4CEC-99C7-1141544CA49B')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'SEYCHELLES')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['ppb_country'], 'UNITED KINGDOM')
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_status(self):
        """Parse foreign entity status"""
        filings = list(lobbyists.parse_filings(util.testpath('foreign_entity_status.xml')))
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '07361BD2-5007-42D6-8794-A7597AECC1B9')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['status'], 'undetermined')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '493C9C11-17ED-4875-88D2-FAC96FF06849')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['status'], 'terminated')
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['status'], 'terminated')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BBF87FC8-73FC-4050-B6F8-850C79EC72E2')
        entities = x['foreign_entities']
        e = entities.pop()['foreign_entity']
        self.failUnlessEqual(e['status'], 'active')
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
