# -*- coding: utf-8 -*-
#
# test_parse_govt_entities.py - Tests for lobbyists govt entity parsing.
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

"""Tests for lobbyists govt entity parsing."""

import unittest
import lobbyists
import util

class TestParseGovtEntities(unittest.TestCase):
    def test_name(self):
        """Parse government entity name"""
        filings = list(lobbyists.parse_filings(util.testpath('government_entity_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '2627E811-33AB-43F4-B8E0-5B979A10FBF9')
        entities = x['govt_entities']
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'UNDETERMINED')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'UNDETERMINED')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'UNDETERMINED')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        entities = x['govt_entities']
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Treasury, Dept of')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Federal Reserve System')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'HOUSE OF REPRESENTATIVES')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Vice President of the U.S.')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Office of Policy Development')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'],
                             'Executive Office of the President (EOP)')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'SENATE')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'White House Office')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '106C2C6E-F0E1-46E3-9409-294E0BD27878')
        entities = x['govt_entities']
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'],
                             'Federal Communications Commission (FCC)')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Environmental Protection Agency (EPA)')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'Energy, Dept of')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'HOUSE OF REPRESENTATIVES')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'],
                             'Federal Energy Regulatory Commission (FERC)')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'SENATE')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'FFF29969-FDEC-4125-809E-0D8D2D8E73FC')
        entities = x['govt_entities']
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'],
                             'Health & Human Services, Dept of  (HHS)')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'SENATE')
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'HOUSE OF REPRESENTATIVES')
        self.failUnlessEqual(len(entities), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'FD29F4AF-763B-42A6-A27E-0AE115CD6D51')
        entities = x['govt_entities']
        e = entities.pop()['govt_entity']
        self.failUnlessEqual(e['name'], 'NONE')
        self.failUnlessEqual(len(entities), 0)

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
