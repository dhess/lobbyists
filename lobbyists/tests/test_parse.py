# -*- coding: utf-8 -*-
#
# test_parse.py - Tests for the lobbyists module parse_* functions.
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

"""Tests for the lobbyists module parse_* functions."""

import unittest
import lobbyists
import util

class TestParseFilings(unittest.TestCase):
    def test_id(self):
        filings = [x for x in lobbyists.parse_filings(util.testpath('ids.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5F787E27-BBF1-45A5-8392-FFF93CCA2746')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D48A20C9-211C-43B1-BBD1-001B075854BA')        
        self.failUnlessEqual(len(filings), 0)
        
    def test_year(self):        
        filings = [x for x in lobbyists.parse_filings(util.testpath('years.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BEE00319-9EC2-4ECF-89F7-75A6436433F1')
        self.failUnlessEqual(f['year'], 2008)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '12B45653-7326-4803-8B86-7538D7CA65AA')
        self.failUnlessEqual(f['year'], 1999)

        self.failUnlessEqual(len(filings), 0)

    def test_filing_date(self):        
        filings = [x for x in lobbyists.parse_filings(util.testpath('filing_dates.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '355A164F-AC36-47EC-AD84-0D4DC2CD579E')
        self.failUnlessEqual(f['filing_date'], '2007-02-13T16:07:28')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '028C0F4E-0B08-465F-BD86-0197F149A77E')
        self.failUnlessEqual(f['filing_date'], '1999-02-08T00:00:00')

        self.failUnlessEqual(len(filings), 0)

    def test_amount(self):        
        filings = [x for x in lobbyists.parse_filings(util.testpath('amounts.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'BAA88635-8674-4DF8-8825-2B0B3D8B4554') 
        self.failUnlessEqual(f['amount'], 108000)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9648F901-BA48-4EE5-BE8B-01D5551BFDA1') 
        self.failUnlessEqual(f['amount'], 20000)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '8F21CC08-E136-4A42-A51D-25FE3B6CC303') 
        self.failUnlessEqual(f['amount'], 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DE669D92-0620-4257-8B0C-01922EA0A226') 
        self.failUnlessEqual(f['amount'], None)  # None means unspecified amount

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5DA4C8F8-4E2D-4EE1-895C-00369A8222FB') 
        self.failUnlessEqual(f['amount'], None)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DB4CCA2C-1E51-46A7-8800-00201697E905') 
        self.failUnlessEqual(f['amount'], None)

        self.failUnlessEqual(len(filings), 0)

    def test_period(self):        
        filings = [x for x in lobbyists.parse_filings(util.testpath('periods.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5B0FD8D4-8718-44D1-B811-0E65BF87D11B')
        self.failUnlessEqual(f['period'], 'H2')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '512736BE-D883-4D5A-BAA3-0A6A08C25C9A')
        self.failUnlessEqual(f['period'], 'H1')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'B71DBB87-C505-49F2-81E9-0060DE66FF9A')
        self.failUnlessEqual(f['period'], 'undetermined')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F219DA64-4F6C-4518-8873-DADDE53728C9')
        self.failUnlessEqual(f['period'], 'Q4')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '490E6C11-39A1-4920-816C-00093F1E6CEB')
        self.failUnlessEqual(f['period'], 'Q2')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '25E651E6-87C9-4D5F-9F92-0329F42B8CDD')
        self.failUnlessEqual(f['period'], 'Q1')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F0DCE4D9-DB4D-44C7-8129-30DCC854447D')
        self.failUnlessEqual(f['period'], 'Q3')
        
        self.failUnlessEqual(len(filings), 0)

    def test_type(self):
        filings = [x for x in lobbyists.parse_filings(util.testpath('types.xml'))]
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '1EC3E96B-5B9D-4D0F-8061-1439D9214744')
        self.failUnlessEqual(f['type'], 'YEAR-END TERMINATION LETTER')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C353F282-13C1-4DE0-B4E8-FA0E31BEBAB7')
        self.failUnlessEqual(f['type'], 'YEAR-END TERMINATION AMENDMENT (NO ACTIVITY)')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '94BDBF44-F819-450E-8B8C-AAC00975C0A0')
        self.failUnlessEqual(f['type'], 'YEAR-END TERMINATION AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DC20B05D-40D7-40C0-A183-8867B1F9FD28')
        self.failUnlessEqual(f['type'], 'YEAR-END TERMINATION (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '579B1110-C307-4BDC-972C-A59707624771')
        self.failUnlessEqual(f['type'], 'YEAR-END TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '64DA0647-6FFD-48C8-B558-C2AB3B88E034')
        self.failUnlessEqual(f['type'], 'YEAR-END REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'ED1B309C-42D4-499E-A30D-B7BD5500662B')
        self.failUnlessEqual(f['type'], 'YEAR-END AMENDMENT (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C385C83E-F0A9-47B0-B922-8AC2E91AFFEC')
        self.failUnlessEqual(f['type'], 'YEAR-END AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CCDB2C62-93E4-4DC3-915B-16C92E7DAAC9')
        self.failUnlessEqual(f['type'], 'YEAR-END (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '49FD659D-841F-436E-A6B5-871292AB77E0')
        self.failUnlessEqual(f['type'], 'THIRD QUARTER TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F0DCE4D9-DB4D-44C7-8129-30DCC854447D')
        self.failUnlessEqual(f['type'], 'THIRD QUARTER REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '2B1526CF-DDFA-47DD-BFD3-D52319CBB085')
        self.failUnlessEqual(f['type'], 'THIRD QUARTER AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CFD5EBE9-E4D3-47F2-8B10-56FE0535ADAA')
        self.failUnlessEqual(f['type'], 'SECOND QUARTER TERMINATION AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '0B596CA7-3ADC-475C-B8D6-3F7D7B2286BB')
        self.failUnlessEqual(f['type'], 'SECOND QUARTER TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'CE7DF2DF-3AFC-4BCA-9FDC-3F8FAE53E812')
        self.failUnlessEqual(f['type'], 'SECOND QUARTER REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'B2BEA33F-7B4C-4E50-95AB-3F7DE8426A59')
        self.failUnlessEqual(f['type'], 'SECOND QUARTER AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '64EE7F0D-4E82-4C8D-B2AC-F4128A90B033')
        self.failUnlessEqual(f['type'], 'REGISTRATION AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '28F649F4-903E-40CE-A7EF-113C3791A05F')
        self.failUnlessEqual(f['type'], 'REGISTRATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '19B38737-5F08-405B-8933-FB3D15EFF1EE')
        self.failUnlessEqual(f['type'], 'MISC. DOC')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '0F840E2B-E9E7-439E-802D-617AD7CB8F29')
        self.failUnlessEqual(f['type'], 'MISC TERM')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '666BB52D-7B0C-40F7-83B9-5ED9C92B97AD')
        self.failUnlessEqual(f['type'], 'MID-YEAR TERMINATION LETTER')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DA0990B8-726B-4013-B340-1A44CBA67634')
        self.failUnlessEqual(f['type'], 'MID-YEAR TERMINATION AMENDMENT (NO ACTIVITY)')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DC179A14-EFD2-4F6B-AD3A-27F6974B398F')
        self.failUnlessEqual(f['type'], 'MID-YEAR TERMINATION AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D6491C4B-7C2D-443E-95F5-2CD43EA08888')
        self.failUnlessEqual(f['type'], 'MID-YEAR TERMINATION (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '87FF6D03-8663-411E-8784-4C8325A257CA')
        self.failUnlessEqual(f['type'], 'MID-YEAR TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'DD9BD48E-59D6-4AE3-88AE-5A3CD79B014E')
        self.failUnlessEqual(f['type'], 'MID-YEAR REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '7961A624-7224-4835-832E-EC3BCA8E66EF')
        self.failUnlessEqual(f['type'], 'MID-YEAR AMENDMENT (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '6A2C1DEE-1672-4194-8C76-B4CD43EDDEDB')
        self.failUnlessEqual(f['type'], 'MID-YEAR AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '8A59C334-E26E-4442-BAB6-0B5ADCF93F94')
        self.failUnlessEqual(f['type'], 'MID-YEAR (NO ACTIVITY)')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D488BE0B-6DC7-433D-B0E0-D71BAC864571')
        self.failUnlessEqual(f['type'], 'FOURTH QUARTER TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F219DA64-4F6C-4518-8873-DADDE53728C9')
        self.failUnlessEqual(f['type'], 'FOURTH QUARTER REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '1A47D643-4777-4270-AAA4-AF998C965E48')
        self.failUnlessEqual(f['type'], 'FOURTH QUARTER AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '0E781869-DE6E-433A-BE8B-3481E38810B8')
        self.failUnlessEqual(f['type'], 'FIRST QUARTER TERMINATION AMENDMENT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '68EBB384-5B72-4987-A028-2DFBE4AF6D0A')
        self.failUnlessEqual(f['type'], 'FIRST QUARTER TERMINATION')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'FE2A0EF2-2E78-457B-BD18-046FBDA102C7')
        self.failUnlessEqual(f['type'], 'FIRST QUARTER REPORT')
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E5857A8B-C78A-42AB-B8E9-032AF4842C73')
        self.failUnlessEqual(f['type'], 'FIRST QUARTER AMENDMENT')
        
        self.failUnlessEqual(len(filings), 0)

    def test_affiliated_orgs_url(self):
        filings = list(lobbyists.parse_filings(util.testpath('filing_affiliated_orgs_url.xml')))
        
        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '493C9C11-17ED-4875-88D2-FAC96FF06849')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             "are the members listed on coalition's website?")

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9B5A4E46-8AAA-4497-B11A-B83B6D18836C')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'www.hklaw.com    www.ppsv.com')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5F456254-75FE-4ED2-8F74-92C169B6800A')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C6EABAE0-1E89-491F-97B3-5282386EC69C')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'www.bnl.gov (Brookhaven Science Association);   www.ut-battelle.org (UT-Battelle)')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '8A3DB5DF-04A3-4002-9353-2C12104A0B49')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'www.wal-mart.com; www.rossstores.com')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '6D4AFEE6-E886-4993-B153-14A887FD325A')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'www.landolakesinc.com              4001 Lexington Ave. N, Arden Hills Minnesota 55112-6943')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'E34132EF-DA6D-40BF-BDEA-D13DBDF09BEA')
        self.failUnlessEqual(f['affiliated_orgs_url'], 'None')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '0C4051F5-2E0A-4ABC-A140-7FAFF7669D00')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'Patton Boggs, LLP, 2550 M. Street N.W., Washington, D.C. 20037 - pfarthing@pattonboggs.com')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        self.failUnlessEqual(f['affiliated_orgs_url'], 'N/A')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C72D65BA-24D0-4AB7-97E4-7D68FD2BCB7D')
        self.failUnlessEqual(f['affiliated_orgs_url'], 'judith_burrell@cox.net')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '09C471E9-2B98-433A-8E4D-0C3928459C20')
        self.failUnlessEqual(f['affiliated_orgs_url'],
                             'http://skipjack.net/le_shore/worcestr/welcome.html')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '16E1EA9C-F6B3-4319-957E-14F4D65BD9F4')
        self.failUnlessEqual(f['affiliated_orgs_url'], 'www.exxonmobile.com')

        self.failUnlessEqual(len(filings), 0)


class TestParseRegistrants(unittest.TestCase):
    def test_address(self):
        filings = [x for x in lobbyists.parse_filings(util.testpath('registrant_addrs.xml'))]

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
        filings = list(lobbyists.parse_filings(util.testpath('registrant_senate_id.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '9CF0D039-7655-4C7E-99E9-00166359FD5B')
        reg = x['registrant']
        self.failUnlessEqual(reg['senate_id'], 287656)

        self.failUnlessEqual(len(filings), 0)

    def test_name(self):
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


class TestParseClients(unittest.TestCase):
    def test_country(self):
        """Parse client country and PPB country"""
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_country.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_id.xml'))]

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'C3226D4B-2F22-4516-BDF2-9E1F918D140E')
        client = x['client']
        self.failUnlessEqual(client['senate_id'], 48)

        self.failUnlessEqual(len(filings), 0)


    def test_name(self):
        """Parse client name"""
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_name.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_state.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_status.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_contact_name.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_description.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('client_state_or_local_gov.xml'))]

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


class TestParseLobbyists(unittest.TestCase):
    def test_name(self):
        """Parse lobbyist name"""
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyist_name.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyist_status.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyist_indicator.xml'))]

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
        filings = [x for x in lobbyists.parse_filings(util.testpath('lobbyist_official_position.xml'))]

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
        

class TestParseGovtEntities(unittest.TestCase):
    def test_name(self):
        """Parse government entity name"""
        filings = [x for x in lobbyists.parse_filings(util.testpath('government_entity_name.xml'))]

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


class TestParseIssues(unittest.TestCase):
    def test_code(self):
        """Parse issue code"""
        filings = list(lobbyists.parse_filings(util.testpath('issue_code.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'BANKING')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'REAL ESTATE/LAND USE/CONSERVATION')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'],
                             'FINANCIAL INSTITUTIONS/INVESTMENTS/SECURITIES')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'FOREIGN RELATIONS')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'],
                             'LAW ENFORCEMENT/CRIME/CRIMINAL JUSTICE')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'FAMILY ISSUES/ABORTION/ADOPTION')
        self.failUnlessEqual(len(issues), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'HEALTH ISSUES')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'MEDICARE/MEDICAID')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'WELFARE')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'BUDGET/APPROPRIATIONS')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'TAXATION/INTERNAL REVENUE CODE')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['code'], 'INSURANCE')
        self.failUnlessEqual(len(issues), 0)

        self.failUnlessEqual(len(filings), 0)

    def test_specific_issue(self):
        """Parse specific issue"""
        filings = list(lobbyists.parse_filings(util.testpath('issue_specific_issue.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'], 'unspecified')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nComprehensive Energy Bill')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nH.R. 1495 Water Resources Development Act (WRDA) - the WRDA provisions to modernize the locks on the Upper Mississippi and Illinois Rivers are essential if U.S. agriculture is going to remain competitive in the global marketplace.\r\nH.R. 1495 the Water Resources Development Act of 2007 (WRDA) - conference report - Title VIII of the legislation includes authorization for the Corps of Engineers to construct new 1,200 foot locks on the Upper Mississippi and Illinois Rivers\n')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nImmigration - Thanking Senator Lincoln and her staff for the hard work and long hours and dedication they presented in an effort to develop a comprehensive immigration reform.\n')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nFY08 Agriculture Appropriations Bill - (Sec. 738) amendment to prohibit USDA from spending money for health inspection of horses.\n\nH.R. 3161, the FY08 Ag spending bill - amendments: King/Kingston amendment to strike Sec. 738. It would limit USDA authority for equine health inspection, effectively restricting the movement of all horses; Ackerman amendment prohibits funding for Food Safety and Inspection Service (FSIS) inspections in facilities that process nonambulatory or downer livestock;  Whitfield-Spratt-Rahall-Chandler amendment to restrict USDA inspection of horses intended for processing for human consumption.\n\nPayment Limits.\r\nFarm Bill: tax title, reductions in direct payments, counter-cyclical revenue option, senate ag committee markup on farm bill, amendments seeking further reform to payment limits and adjusted gross income restrictions.\n')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nU.S. -Peru Trade Promotion Agreement (TPA) - the goal is to increase U.S. agriculture exports and increase market share.')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nFY08 Labor, HHS and Education spending.  Perkins Amendment (federal funding for FFA and career and technical education).')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             '\r\nH.R. 3098 to restore farm truck exemptions from federal motor carrier vehicle regulations.')
        self.failUnlessEqual(len(issues), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '05804BE5-57C9-41BF-97B2-0120826D4393')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\n')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\nH.R.2638 & S.1644 FY08 DHS AppropriationsBill-CRP')
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\nH.R.2638 & S.1644 FY08 DHS AppropriationsBill-CRP')

        self.failUnlessEqual(len(issues), 0)

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'F56492FC-4FBD-4824-83E1-0004B30F0519')
        issues = x['issues']
        i = issues.pop()['issue']
        self.failUnlessEqual(i['specific_issue'],
                             'DEFENSE AUTHORIZATION, DEFENSE APPROPRIATIONS, VETERANS, DEFENSE HEALTH CARE, ARMED FORCES RETIREMENT, ARMED FORCES PERSONNEL BENEFITS, EMERGING DEFENSE RELATED ISSUES')
        self.failUnlessEqual(len(issues), 0)

        self.failUnlessEqual(len(filings), 0)


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
