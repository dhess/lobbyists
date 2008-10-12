# -*- coding: utf-8 -*-
#
# test_parse_filings.py - Tests for lobbyists.parse_filings.
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

"""Tests for lobbyists.parse_filings."""

import unittest
import lobbyists
import util

class TestParseFilings(unittest.TestCase):
    def test_id(self):
        """Parse filing id"""
        filings = list(lobbyists.parse_filings(util.testpath('ids.xml')))

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], '5F787E27-BBF1-45A5-8392-FFF93CCA2746')

        x = filings.pop()
        f = x['filing']
        self.failUnlessEqual(f['id'], 'D48A20C9-211C-43B1-BBD1-001B075854BA')        
        self.failUnlessEqual(len(filings), 0)
        
    def test_year(self):
        """Parse filing year"""
        filings = list(lobbyists.parse_filings(util.testpath('years.xml')))

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
        """Parse filing filing date"""
        filings = list(lobbyists.parse_filings(util.testpath('filing_dates.xml')))

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
        """Parse filing amount"""
        filings = list(lobbyists.parse_filings(util.testpath('amounts.xml')))

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
        """Parse filing period"""
        filings = list(lobbyists.parse_filings(util.testpath('periods.xml')))

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
        """Parse filing type"""
        filings = list(lobbyists.parse_filings(util.testpath('types.xml')))
        
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
        """Parse filing affiliated orgs URL"""
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


if __name__ == '__main__':
    unittest.main()
