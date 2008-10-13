# -*- coding: utf-8 -*-
#
# test_parse_affiliated_orgs.py - Tests for lobbyists affiliated orgs parsing.
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

"""Tests for lobbyists affiliated orgs parsing."""

import unittest
import lobbyists
import util


class TestParseAffiliatedOrgs(unittest.TestCase):
    def test_name(self):
        """Parse affiliated org name"""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_org_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E8A4D9C9-2D0B-4F0A-966D-A076858D2751')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], 'N/A')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], 'CARITAS CHRISTI')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], 'BOSTON MEDICAL CENTER')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], 'PARTNERS HEALTHCARE SYSTEM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], 'DANA FARBER CANCER INSTITUTE')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '6D4AFEE6-E886-4993-B153-14A887FD325A')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['name'], "Land O'Lakes, Inc.")

        self.failUnlessEqual(len(filings), 0)

    def test_country(self):
        """Parse affiliated org country"""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_org_country.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '373B396A-51A9-42F6-AAB2-0CBF69177C43')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'NETHERLANDS')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'FRANCE')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'FRANCE')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F0054303-E42F-48CE-8D71-CE7B2FBE8707')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'PUERTO RICO')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A4F6A122-5550-46AF-9C5C-2838FF6538FE')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'unspecified')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A0AA1F41-447E-4A0B-B09A-B0C24645F805')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNDETERMINED')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E63105D4-9840-492D-A81E-F6816CBAFACE')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9B506978-9D51-431A-A698-11F682485512')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_ppb_country(self):
        """Parse affiliated org PPB country"""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_org_country.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '373B396A-51A9-42F6-AAB2-0CBF69177C43')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], '<SELECT ONE>')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F0054303-E42F-48CE-8D71-CE7B2FBE8707')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'PUERTO RICO')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A4F6A122-5550-46AF-9C5C-2838FF6538FE')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'UNDETERMINED')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A0AA1F41-447E-4A0B-B09A-B0C24645F805')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E63105D4-9840-492D-A81E-F6816CBAFACE')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'UNDETERMINED')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9B506978-9D51-431A-A698-11F682485512')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        orgs = x['affiliated_orgs']
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        o = orgs.pop()['org']
        self.failUnlessEqual(o['ppb_country'], 'USA')
        self.failUnlessEqual(len(orgs), 0)

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
