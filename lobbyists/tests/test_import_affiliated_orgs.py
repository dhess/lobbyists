# -*- coding: utf-8 -*-
#
# test_import_affiliated_orgs.py - Test affiliated org importing.
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

"""Test affiliated org importing."""

import unittest
import lobbyists
import sqlite3
import util

class TestImportAffiliatedOrgs(unittest.TestCase):
    def test_import_affiliated_orgs(self):
        """Import affiliated orgs"""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM affiliated_org")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['id'], 31)
        self.failUnlessEqual(row['name'], 'PORTAL DEL FUTURO AUTHORITY')
        self.failUnlessEqual(row['country'], 'PUERTO RICO')
        self.failUnlessEqual(row['ppb_country'], 'PUERTO RICO')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 30)
        self.failUnlessEqual(row['name'], 'ITNL EMISSIONS TRADING ASSN')
        self.failUnlessEqual(row['country'], 'unspecified')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 29)
        self.failUnlessEqual(row['name'], 'ISL')
        self.failUnlessEqual(row['country'], 'UNDETERMINED')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 28)
        self.failUnlessEqual(row['name'], 'CHILDRENS HOSPITAL OAKLAND')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 27)
        self.failUnlessEqual(row['name'], 'INMARSAT LTD')
        self.failUnlessEqual(row['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 26)
        self.failUnlessEqual(row['name'], 'UC GROUP LIMITED')
        self.failUnlessEqual(row['country'], 'UNITED KINGDOM')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 25)
        self.failUnlessEqual(row['name'], 'N/A')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 24)
        self.failUnlessEqual(row['name'], 'Time Warner Cable')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 23)
        self.failUnlessEqual(row['name'], 'Palm, Inc.')
        self.failUnlessEqual(row['country'], '<SELECT ONE>')
        self.failUnlessEqual(row['ppb_country'], '<SELECT ONE>')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 22)
        self.failUnlessEqual(row['name'], 'Warner Bros.')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 21)
        self.failUnlessEqual(row['name'], 'AOL')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 20)
        self.failUnlessEqual(row['name'], 'Power Pyles Sutter & Verville')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 19)
        self.failUnlessEqual(row['name'], 'Holland and Knight')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 18)
        self.failUnlessEqual(row['name'], 'HCR ManorCare')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 17)
        self.failUnlessEqual(row['name'], 'Vitas')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 16)
        self.failUnlessEqual(row['name'], 'Odyssey')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 15)
        self.failUnlessEqual(row['name'], 'AseraCare')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 14)
        self.failUnlessEqual(row['name'], 'UT-Battelle')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 13)
        self.failUnlessEqual(row['name'], 'Brookhaven Science Association')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 12)
        self.failUnlessEqual(row['name'], 'Ross Stores, Inc.')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 11)
        self.failUnlessEqual(row['name'], 'Wal-Mart Stores, Inc.')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 10)
        self.failUnlessEqual(row['name'], "Land O'Lakes, Inc.")
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 9)
        self.failUnlessEqual(row['name'], 'SOUTHEASTERN FEDERAL POWER CUSTOME')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 8)
        self.failUnlessEqual(row['name'], 'Patton Boggs, LLP')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 7)
        self.failUnlessEqual(row['name'], 'CARITAS CHRISTI')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 6)
        self.failUnlessEqual(row['name'], 'BOSTON MEDICAL CENTER')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 5)
        self.failUnlessEqual(row['name'], 'PARTNERS HEALTHCARE SYSTEM')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 4)
        self.failUnlessEqual(row['name'], 'DANA FARBER CANCER INSTITUTE')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 3)
        self.failUnlessEqual(row['name'], 'ORANGE COUNTY TRANSPORTATION AUTHOR')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 2)
        self.failUnlessEqual(row['name'], 'JERRY REDDEN')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 1)
        self.failUnlessEqual(row['name'], 'EXXONMOBILE')
        self.failUnlessEqual(row['country'], 'USA')
        self.failUnlessEqual(row['ppb_country'], 'USA')

        self.failUnlessEqual(len(rows), 0)

    def test_import_filings_to_affiliated_orgs(self):
        """Affiliated orgs are matched up with filings in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_affiliated_orgs")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'F0054303-E42F-48CE-8D71-CE7B2FBE8707')
        self.failUnlessEqual(row['org'], 31)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A4F6A122-5550-46AF-9C5C-2838FF6538FE')
        self.failUnlessEqual(row['org'], 30)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A0AA1F41-447E-4A0B-B09A-B0C24645F805')
        self.failUnlessEqual(row['org'], 29)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'A0AA1F41-447E-4A0B-B09A-B0C24645F805')
        self.failUnlessEqual(row['org'], 28)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'E63105D4-9840-492D-A81E-F6816CBAFACE')
        self.failUnlessEqual(row['org'], 27)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '9B506978-9D51-431A-A698-11F682485512')
        self.failUnlessEqual(row['org'], 26)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'E8A4D9C9-2D0B-4F0A-966D-A076858D2751')
        self.failUnlessEqual(row['org'], 25)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '493C9C11-17ED-4875-88D2-FAC96FF06849')
        self.failUnlessEqual(row['org'], 24)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '493C9C11-17ED-4875-88D2-FAC96FF06849')
        self.failUnlessEqual(row['org'], 23)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '493C9C11-17ED-4875-88D2-FAC96FF06849')
        self.failUnlessEqual(row['org'], 22)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '493C9C11-17ED-4875-88D2-FAC96FF06849')
        self.failUnlessEqual(row['org'], 21)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '9B5A4E46-8AAA-4497-B11A-B83B6D18836C')
        self.failUnlessEqual(row['org'], 20)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '9B5A4E46-8AAA-4497-B11A-B83B6D18836C')
        self.failUnlessEqual(row['org'], 19)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '5F456254-75FE-4ED2-8F74-92C169B6800A')
        self.failUnlessEqual(row['org'], 18)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '5F456254-75FE-4ED2-8F74-92C169B6800A')
        self.failUnlessEqual(row['org'], 17)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '5F456254-75FE-4ED2-8F74-92C169B6800A')
        self.failUnlessEqual(row['org'], 16)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '5F456254-75FE-4ED2-8F74-92C169B6800A')
        self.failUnlessEqual(row['org'], 15)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C6EABAE0-1E89-491F-97B3-5282386EC69C')
        self.failUnlessEqual(row['org'], 14)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C6EABAE0-1E89-491F-97B3-5282386EC69C')
        self.failUnlessEqual(row['org'], 13)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '8A3DB5DF-04A3-4002-9353-2C12104A0B49')
        self.failUnlessEqual(row['org'], 12)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '8A3DB5DF-04A3-4002-9353-2C12104A0B49')
        self.failUnlessEqual(row['org'], 11)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '6D4AFEE6-E886-4993-B153-14A887FD325A')
        self.failUnlessEqual(row['org'], 10)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'E34132EF-DA6D-40BF-BDEA-D13DBDF09BEA')
        self.failUnlessEqual(row['org'], 9)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '0C4051F5-2E0A-4ABC-A140-7FAFF7669D00')
        self.failUnlessEqual(row['org'], 8)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        self.failUnlessEqual(row['org'], 7)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        self.failUnlessEqual(row['org'], 6)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        self.failUnlessEqual(row['org'], 5)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C8293344-9A8D-4D6F-AAA5-25925E60BED9')
        self.failUnlessEqual(row['org'], 4)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             'C72D65BA-24D0-4AB7-97E4-7D68FD2BCB7D')
        self.failUnlessEqual(row['org'], 3)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '09C471E9-2B98-433A-8E4D-0C3928459C20')
        self.failUnlessEqual(row['org'], 2)

        row = rows.pop()
        self.failUnlessEqual(row['filing'],
                             '16E1EA9C-F6B3-4319-957E-14F4D65BD9F4')
        self.failUnlessEqual(row['org'], 1)

        self.failUnlessEqual(len(rows), 0)
        
    def test_import_affiliated_org_to_urls(self):
        """Affiliated orgs are matched up with URLs in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM affiliated_org_urls")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['org'], 31)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 30)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 29)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 28)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 27)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 26)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 25)
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 24)
        self.failUnlessEqual(row['url'],
                             "are the members listed on coalition's website?")

        row = rows.pop()
        self.failUnlessEqual(row['org'], 23)
        self.failUnlessEqual(row['url'],
                             "are the members listed on coalition's website?")

        row = rows.pop()
        self.failUnlessEqual(row['org'], 22)
        self.failUnlessEqual(row['url'],
                             "are the members listed on coalition's website?")

        row = rows.pop()
        self.failUnlessEqual(row['org'], 21)
        self.failUnlessEqual(row['url'],
                             "are the members listed on coalition's website?")

        row = rows.pop()
        self.failUnlessEqual(row['org'], 20)
        self.failUnlessEqual(row['url'],
                             'www.hklaw.com    www.ppsv.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 19)
        self.failUnlessEqual(row['url'],
                             'www.hklaw.com    www.ppsv.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 18)
        self.failUnlessEqual(row['url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 17)
        self.failUnlessEqual(row['url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 16)
        self.failUnlessEqual(row['url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 15)
        self.failUnlessEqual(row['url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 14)
        self.failUnlessEqual(row['url'],
                             'www.bnl.gov (Brookhaven Science Association);   www.ut-battelle.org (UT-Battelle)')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 13)
        self.failUnlessEqual(row['url'],
                             'www.bnl.gov (Brookhaven Science Association);   www.ut-battelle.org (UT-Battelle)')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 12)
        self.failUnlessEqual(row['url'],
                             'www.wal-mart.com; www.rossstores.com')

        row = rows.pop()
        self.failUnlessEqual(row['org'], 11)
        self.failUnlessEqual(row['url'],
                             'www.wal-mart.com; www.rossstores.com')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 10)
        self.failUnlessEqual(row['url'],
                             'www.landolakesinc.com              4001 Lexington Ave. N, Arden Hills Minnesota 55112-6943')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 9)
        self.failUnlessEqual(row['url'], 'None')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 8)
        self.failUnlessEqual(row['url'],
                             'Patton Boggs, LLP, 2550 M. Street N.W., Washington, D.C. 20037 - pfarthing@pattonboggs.com')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 7)
        self.failUnlessEqual(row['url'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 6)
        self.failUnlessEqual(row['url'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 5)
        self.failUnlessEqual(row['url'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 4)
        self.failUnlessEqual(row['url'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 3)
        self.failUnlessEqual(row['url'],  'judith_burrell@cox.net')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 2)
        self.failUnlessEqual(row['url'],
                             'http://skipjack.net/le_shore/worcestr/welcome.html')
        
        row = rows.pop()
        self.failUnlessEqual(row['org'], 1)
        self.failUnlessEqual(row['url'], 'www.exxonmobile.com')
        
        self.failUnlessEqual(len(rows), 0)

    def test_import_affiliated_orgs_org(self):
        """Importing affiliated orgs should fill the 'org' table."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM org")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'PORTAL DEL FUTURO AUTHORITY')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'ITNL EMISSIONS TRADING ASSN')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'ISL')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'CHILDRENS HOSPITAL OAKLAND')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'INMARSAT LTD')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UC GROUP LIMITED')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'N/A')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Time Warner Cable')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Palm, Inc.')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Warner Bros.')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'AOL')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Power Pyles Sutter & Verville')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Holland and Knight')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'HCR ManorCare')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Vitas')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Odyssey')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'AseraCare')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UT-Battelle')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Brookhaven Science Association')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Ross Stores, Inc.')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Wal-Mart Stores, Inc.')

        row = rows.pop()
        self.failUnlessEqual(row['name'], "Land O'Lakes, Inc.")

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'SOUTHEASTERN FEDERAL POWER CUSTOME')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'Patton Boggs, LLP')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'CARITAS CHRISTI')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'BOSTON MEDICAL CENTER')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'PARTNERS HEALTHCARE SYSTEM')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'DANA FARBER CANCER INSTITUTE')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'ORANGE COUNTY TRANSPORTATION AUTHOR')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'JERRY REDDEN')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'EXXONMOBILE')

        self.failUnlessEqual(len(rows), 0)

    def test_import_affiliated_orgs_country(self):
        """Importing affiliated orgs should fill the 'country' table."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM country")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'PUERTO RICO')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UNITED KINGDOM')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'UNDETERMINED')

        row = rows.pop()
        self.failUnlessEqual(row['name'], '<SELECT ONE>')

        row = rows.pop()
        self.failUnlessEqual(row['name'], 'USA')

        self.failUnlessEqual(len(rows), 0)

    def test_import_affiliated_org_urls(self):
        """Importing affiliated orgs should fill the 'url' table."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM url")
        rows = [row for row in cur]

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             "are the members listed on coalition's website?")

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'www.hklaw.com    www.ppsv.com')

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'www.vitas.com, www.odyssey-healthcare.com, www.hcr-manorcare.com/home, www.aseracare.com')

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'www.bnl.gov (Brookhaven Science Association);   www.ut-battelle.org (UT-Battelle)')

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'www.wal-mart.com; www.rossstores.com')

        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'www.landolakesinc.com              4001 Lexington Ave. N, Arden Hills Minnesota 55112-6943')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'], 'None')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'Patton Boggs, LLP, 2550 M. Street N.W., Washington, D.C. 20037 - pfarthing@pattonboggs.com')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'], 'N/A')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'],  'judith_burrell@cox.net')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'],
                             'http://skipjack.net/le_shore/worcestr/welcome.html')
        
        row = rows.pop()
        self.failUnlessEqual(row['url'], 'www.exxonmobile.com')
        
        self.failUnlessEqual(len(rows), 0)

    def test_import_identical_affiliated_orgs(self):
        """Identical affiliated orgs shouldn't be duplicated in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs_dup.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT org FROM filing_affiliated_orgs')
        row1, row2 = cur.fetchall()
        self.failUnlessEqual(row1[0], row2[0])

    def test_import_similar_affiliated_orgs(self):
        """Slightly different affiliated orgs are inserted into different rows."""
        filings = list(lobbyists.parse_filings(util.testpath('affiliated_orgs_slightly_different.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))
        cur = con.cursor()
        cur.execute('SELECT id FROM affiliated_org')
        orgs = util.flatten([x['affiliated_orgs'] for x in filings if 'affiliated_orgs' in x])
        self.failUnlessEqual(len(cur.fetchall()), len(orgs))


if __name__ == '__main__':
    unittest.main()
