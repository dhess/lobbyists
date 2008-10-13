# -*- coding: utf-8 -*-
#
# test_parse_clients.py - Tests for lobbyists client parsing.
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

"""Tests for lobbyists client parsing."""

import unittest
import lobbyists
import util


class TestParseClients(unittest.TestCase):
    def test_country(self):
        """Parse client country and PPB country"""
        filings = list(lobbyists.parse_filings(util.testpath('client_country.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '62114C8C-2868-4FD8-AC6A-8CB2C3D64307')
        client = x['client']
        self.failUnlessEqual(client['country'], 'unspecified')
        self.failUnlessEqual(client['ppb_country'], 'USA')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '15A2AECC-B034-42D7-B447-27E70284F3DB')
        client = x['client']
        self.failUnlessEqual(client['country'], '<SELECT ONE>')
        self.failUnlessEqual(client['ppb_country'], '<SELECT ONE>')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '104313A3-968E-478E-870B-9DD28A3E02C4')
        client = x['client']
        self.failUnlessEqual(client['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(client['ppb_country'], 'USA')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '7DB2EC06-677B-4BA3-ACCF-4855C6E112C3')
        client = x['client']
        self.failUnlessEqual(client['country'], 'USA')
        self.failUnlessEqual(client['ppb_country'], 'UNITED KINGDOM')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CFC6E2B6-3A98-4D4B-A239-000B62C084CC')
        client = x['client']
        self.failUnlessEqual(client['country'], 'UNDETERMINED')
        self.failUnlessEqual(client['ppb_country'], 'UNDETERMINED')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '63FC1581-591E-483A-A5D8-24071BE8DEBE')
        client = x['client']
        self.failUnlessEqual(client['country'], 'PUERTO RICO')
        self.failUnlessEqual(client['ppb_country'], 'PUERTO RICO')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '539731C9-3393-4B0B-A6DB-1E1B613C641B')
        client = x['client']
        self.failUnlessEqual(client['country'], 'MEXICO')
        self.failUnlessEqual(client['ppb_country'], 'MEXICO')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '77CC99B3-FFD7-435D-9507-010548438B6F')
        client = x['client']
        self.failUnlessEqual(client['country'], 'USA')
        self.failUnlessEqual(client['ppb_country'], 'USA')

        self.failUnlessEqual(len(filings), 0)

    def test_id(self):
        """Parse client ID"""
        filings = list(lobbyists.parse_filings(util.testpath('client_id.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C3226D4B-2F22-4516-BDF2-9E1F918D140E')
        client = x['client']
        self.failUnlessEqual(client['senate_id'], 48)

        self.failUnlessEqual(len(filings), 0)


    def test_name(self):
        """Parse client name"""
        filings = list(lobbyists.parse_filings(util.testpath('client_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5A4F7B14-D143-4B57-A345-34296865C20D')
        client = x['client']
        self.failUnlessEqual(client['name'], 'Microsoft')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '357D6040-8761-42CB-94C9-0A27C088091E')
        client = x['client']
        self.failUnlessEqual(client['name'], 'COMPUTER & COMMUNICATIONS INDUSTRY ASSN')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '240EDC03-05F3-4F04-9F4B-0018BF4651F1')
        client = x['client']
        self.failUnlessEqual(client['name'], 'AUTOMATIC DATA PROCESSING, INC.')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '583E1BE3-1B7E-4357-A6C8-00125C7DE22D')
        client = x['client']
        self.failUnlessEqual(client['name'], 'EMPRESA BRASILEIRA DE AERONAUTICA SA (EMBRAER)')

        self.failUnlessEqual(len(filings), 0)


    def test_state(self):
        """Parse client state and PPB state"""
        filings = list(lobbyists.parse_filings(util.testpath('client_state.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '36C7C2ED-A81D-4EC9-9270-24882C2D99F1')
        client = x['client']
        self.failUnlessEqual(client['state'], 'unspecified')
        self.failUnlessEqual(client['ppb_state'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5FED9056-BDB0-4738-9F25-243242AE0E3B')
        client = x['client']
        self.failUnlessEqual(client['state'], 'UNDETERMINED')
        self.failUnlessEqual(client['ppb_state'], 'UNDETERMINED')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '104313A3-968E-478E-870B-9DD28A3E02C4')
        client = x['client']
        self.failUnlessEqual(client['state'], 'unspecified')
        self.failUnlessEqual(client['ppb_state'], 'UNDETERMINED')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '296B5A74-B4B0-4F51-A7FD-16D8195C3A2E')
        client = x['client']
        self.failUnlessEqual(client['state'], 'unspecified')
        self.failUnlessEqual(client['ppb_state'], 'NEW YORK')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '7DB2EC06-677B-4BA3-ACCF-4855C6E112C3')
        client = x['client']
        self.failUnlessEqual(client['state'], 'VIRGINIA')
        self.failUnlessEqual(client['ppb_state'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CFC6E2B6-3A98-4D4B-A239-000B62C084CC')
        client = x['client']
        self.failUnlessEqual(client['state'], 'unspecified')
        self.failUnlessEqual(client['ppb_state'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '539731C9-3393-4B0B-A6DB-1E1B613C641B')
        client = x['client']
        self.failUnlessEqual(client['state'], 'unspecified')
        self.failUnlessEqual(client['ppb_state'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '7425914C-E115-4449-B977-0722455B4463')
        client = x['client']
        self.failUnlessEqual(client['state'], 'PUERTO RICO')
        self.failUnlessEqual(client['ppb_state'], 'PUERTO RICO')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '3C6F64C0-4AC8-4E08-AE55-5A8B0E3BB91E')
        client = x['client']
        self.failUnlessEqual(client['state'], 'DISTRICT OF COLUMBIA')
        self.failUnlessEqual(client['ppb_state'], 'DISTRICT OF COLUMBIA')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '77CC99B3-FFD7-435D-9507-010548438B6F')
        client = x['client']
        self.failUnlessEqual(client['state'], 'IDAHO')
        self.failUnlessEqual(client['ppb_state'], 'IDAHO')

        self.failUnlessEqual(len(filings), 0)


    def test_status(self):
        """Parse client status"""
        filings = list(lobbyists.parse_filings(util.testpath('client_status.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '357D6040-8761-42CB-94C9-0A27C088091E')
        client = x['client']
        self.failUnlessEqual(client['status'], 'administratively terminated')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '240EDC03-05F3-4F04-9F4B-0018BF4651F1')
        client = x['client']
        self.failUnlessEqual(client['status'], 'terminated')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '583E1BE3-1B7E-4357-A6C8-00125C7DE22D')
        client = x['client']
        self.failUnlessEqual(client['status'], 'active')

        self.failUnlessEqual(len(filings), 0)


    def test_contact_name(self):
        """Parse client contact name"""
        filings = list(lobbyists.parse_filings(util.testpath('client_contact_name.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '500D51F8-7D36-44D1-B196-9A96A892921A')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '66439336-A74C-41AE-8659-D1A6140D1494')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'L.A. (SKIP) BAFALIS')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '810A9431-7235-4FEB-9A33-08214322E37F')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'JOHN G. BURKE "TOBY"')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5A4F7B14-D143-4B57-A345-34296865C20D')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'JR KIRKLAND')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '357D6040-8761-42CB-94C9-0A27C088091E')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'DANIEL JOHNSON')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '583E1BE3-1B7E-4357-A6C8-00125C7DE22D')
        client = x['client']
        self.failUnlessEqual(client['contact_name'], 'JAMES B. CHRISTIAN')

        self.failUnlessEqual(len(filings), 0)


    def test_description(self):
        """Parse client description"""
        filings = list(lobbyists.parse_filings(util.testpath('client_description.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CCB41994-81FB-4C32-A155-082164564403')
        client = x['client']
        self.failUnlessEqual(client['description'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BD57AEBC-D1D7-4867-880E-0711F5AABD17')
        client = x['client']
        self.failUnlessEqual(client['description'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '530238AB-4144-484F-8297-00D4A969779C')
        client = x['client']
        self.failUnlessEqual(client['description'], 'DISABILITY RESEARCH')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '1402A175-987F-4896-B0F5-00107EF69834')
        client = x['client']
        self.failUnlessEqual(client['description'], 'Distributor of tactical clothing and gear for the military and law enforcement.')

        self.failUnlessEqual(len(filings), 0)


    def test_state_or_local_gov(self):
        "Parse client state or local government status"""
        filings = list(lobbyists.parse_filings(util.testpath('client_state_or_local_gov.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '31733890-2D8D-414E-8EF1-08701CBC5871')
        client = x['client']
        self.failUnlessEqual(client['state_or_local_gov'], 'y')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '045E8E33-BBEA-437C-844D-D1D6057AA2A0')
        client = x['client']
        self.failUnlessEqual(client['state_or_local_gov'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '8949C958-ABF0-49B8-8ACF-0026E92C2B13')
        client = x['client']
        self.failUnlessEqual(client['state_or_local_gov'], 'n')

        self.failUnlessEqual(len(filings), 0)


if __name__ == '__main__':
    unittest.main()
