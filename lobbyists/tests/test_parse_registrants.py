# -*- coding: utf-8 -*-
#
# test_parse_registrants.py - Tests for lobbyists registrant parsing.
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

"""Tests for lobbyists registrant parsing."""

import unittest
import lobbyists
import util


class TestParseRegistrants(unittest.TestCase):
    def test_address(self):
        """Parse registrant address"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_addrs.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D3EEF6D2-FE0B-4A03-A633-AAA16C50BE89')
        reg = x['registrant']
        self.failUnlessEqual(reg['address'],
                             'Waterside P. O. Box 365\r\nHarmondworth, West Drayto\r\nBE\r\nBELGIUM')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D4AFC576-0B22-4CE7-B595-141BE8ABC8DC')
        reg = x['registrant']
        self.failUnlessEqual(reg['address'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CD6A4955-8D7B-44C4-A3E4-00603FAC03A3')
        reg = x['registrant']
        self.failUnlessEqual(reg['address'],
                             '101 Constitution Avenue, NW\r\nSuite 600 West\r\nWashington, DC 20001')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D97EF71E-9062-42A9-9510-00048B943421')
        reg = x['registrant']
        self.failUnlessEqual(reg['address'],
                             '8 HERBERT STREET\r\nALEXANDRIA, VA 22305')

        self.failUnlessEqual(len(filings), 0)

    def test_description(self):
        """Parse registrant description"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_descriptions.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C35AF239-B3BF-45A8-A5F0-11B73F8C7D64')
        reg = x['registrant']
        self.failUnlessEqual(reg['description'],
                             u'Government Relations & Strategic Consulting')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D0325DF2-82F6-4FF1-8C72-08B9CC3E99D7')
        reg = x['registrant']
        self.failUnlessEqual(reg['description'],
                             'defense/energy/interior consulting')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '443C63BC-F0DB-41F7-B912-002CABBF0CAD')
        reg = x['registrant']
        self.failUnlessEqual(reg['description'], 'unspecified')

        self.failUnlessEqual(len(filings), 0)

    def test_country(self):
        """Parse registrant country"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_country.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9B69F104-60E7-4704-9757-AFE7D14A27C3')
        reg = x['registrant']
        self.failUnlessEqual(reg['country'], 'UNDETERMINED')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D3EEF6D2-FE0B-4A03-A633-AAA16C50BE89')
        reg = x['registrant']
        self.failUnlessEqual(reg['country'], 'BELGIUM')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A6D2238A-9786-428F-9CF9-13A460DE4560')
        reg = x['registrant']
        self.failUnlessEqual(reg['country'], 'USA')

        self.failUnlessEqual(len(filings), 0)

    def test_senate_id(self):
        """Parse registrant Senate ID"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_senate_id.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9CF0D039-7655-4C7E-99E9-00166359FD5B')
        reg = x['registrant']
        self.failUnlessEqual(reg['senate_id'], 287656)

        self.failUnlessEqual(len(filings), 0)

    def test_name(self):
        """Parse registrant name"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'FB4267F6-F8CF-43EB-BF47-01EAACD4FAC0')
        reg = x['registrant']
        self.failUnlessEqual(reg['name'], 'CHAFE, BONNIE L.')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '03F5D9EE-5EDD-4ACA-8766-0503753C3C1D')
        reg = x['registrant']
        self.failUnlessEqual(reg['name'], u'Crowell & Moring LLP')

        self.failUnlessEqual(len(filings), 0)

    def test_ppb_country(self):
        """Parse registrant PPB country"""
        filings = list(lobbyists.parse_filings(util.testpath('registrant_country.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9B69F104-60E7-4704-9757-AFE7D14A27C3')
        reg = x['registrant']
        self.failUnlessEqual(reg['ppb_country'], 'UNDETERMINED')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D3EEF6D2-FE0B-4A03-A633-AAA16C50BE89')
        reg = x['registrant']
        self.failUnlessEqual(reg['ppb_country'], 'UNITED KINGDOM')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A6D2238A-9786-428F-9CF9-13A460DE4560')
        reg = x['registrant']
        self.failUnlessEqual(reg['ppb_country'], 'USA')

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
