# -*- coding: utf-8 -*-
#
# test_parse_lobbyists.py - Tests for lobbyists lobbyist parsing.
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

"""Tests for lobbyists lobbyist parsing."""

import unittest
import lobbyists
import util


class TestParseLobbyists(unittest.TestCase):
    def test_name(self):
        """Parse lobbyist name"""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyist_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '87A30FA6-7C35-4294-BA43-4CE7B5B808B3')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'LEHMAN (MY 2006), PATRICK')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'AB94AB3D-F5D6-4EE8-A462-0925A6D9A499')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'LIEN, RICHARD')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'VEITH, SALLY W.')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'BROWER, RONALD')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'HIRST, RICHARD')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'NEWMAN, ANDREA FISCHER')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'GRANESE, LARRY')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'STEENLAND, DOUGLAS M.')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'AILOR, DIANE')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'QUERN, DARRIN')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'SKWAREK, DANIEL')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'ROSIA, MEGAN')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'AMANTE, CAROL')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'FOUSHEE, CLAY')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'MISHKIN, DAVID')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'LIEN, RICHARD')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'BETHKE, CECILIA')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'VAN DE WATER, READ')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'LONG, MARK')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'ROSIA, MEGAN RAE')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'CLIFFORD, DENNY')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'FOUSHES, CLAY')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'SEIDEN, ELLIOTT')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '0FC23296-F948-43FD-98D4-0912F6579E6A')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'NEAL, KATIE')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'NEAL, KATIE')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'NEAL, KATIE')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D97EF71E-9062-42A9-9510-00048B943421')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'LEVI, ROBERT')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '02DDA99B-725A-4DBA-8397-34892A6918D7')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'unspecified')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'MCKENNEY, WILLIAM')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'WILLCOX, LAWRENCE')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'HOOPER, LINDSAY')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'MIKRUT, JOSEPH')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'TALISMAN, JONATHAN')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'DENNIS, JAMES')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['name'], 'GRAFMEYER, RICHARD')
        self.failUnlessEqual(len(lobbiers), 0)

        self.failUnlessEqual(len(filings), 0)


    def test_status(self):
        """Parse lobbyist status"""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyist_status.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '02DDA99B-725A-4DBA-8397-34892A6918D7')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['status'], 'terminated')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'AB94AB3D-F5D6-4EE8-A462-0925A6D9A499')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['status'], 'active')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['status'], 'terminated')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '04926911-8A12-4A0E-9DA4-510869446EAC')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['status'], 'undetermined')
        self.failUnlessEqual(len(lobbiers), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_indicator(self):
        """Parse lobbyist 'indicator'"""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyist_indicator.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C24ECC15-204A-4146-AB8F-6B3F92099CB5')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '771F3B6A-315D-4190-88F3-2CE0F138B2B8')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '02DDA99B-725A-4DBA-8397-34892A6918D7')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'AB94AB3D-F5D6-4EE8-A462-0925A6D9A499')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BD894C51-AA23-46AE-9802-006B8C91702B')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DE038A45-9F6B-4764-B678-8004E7903BC4')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'not covered')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '2164D6BB-EBBA-40D2-9C18-16A2D670030A')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'covered')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['indicator'], 'undetermined')
        self.failUnlessEqual(len(lobbiers), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_official_position(self):
        """Parse lobbyist 'official position'"""
        filings = list(lobbyists.parse_filings(util.testpath('lobbyist_official_position.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'AB94AB3D-F5D6-4EE8-A462-0925A6D9A499')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'],
                             'MGR. AIR TRAFFIC DIV. WEST PAC, REG, FAA')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BD894C51-AA23-46AE-9802-006B8C91702B')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'],
                             'ExecFlrAsst, H. Maj. Whip; ExecDir, H.DemCauc.')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'],
                             'StaffAsst, DemPolicyComm; FlrAsst, MinoritySec')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'],
                             'Chief of Staff, President Reagan')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'],
                             'AsstEditor/Ed./Res.Dir, Sen.Rep.PolicyComm;')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DE038A45-9F6B-4764-B678-8004E7903BC4')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'unspecified')
        self.failUnlessEqual(len(lobbiers), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '2164D6BB-EBBA-40D2-9C18-16A2D670030A')
        lobbiers = x['lobbyists']
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        l = lobbiers.pop()['lobbyist']
        self.failUnlessEqual(l['official_position'], 'N/A')
        self.failUnlessEqual(len(lobbiers), 0)

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
