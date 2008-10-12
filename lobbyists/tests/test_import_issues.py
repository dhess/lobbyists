# -*- coding: utf-8 -*-
#
# test_import_issues.py - Test issue importing.
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

"""Test issue importing."""

import unittest
import lobbyists
import sqlite3
import util

class TestImportIssues(unittest.TestCase):
    def test_import_issues(self):
        """Import issues"""
        filings = list(lobbyists.parse_filings(util.testpath('issues.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM issue")
        rows = list(cur)

        row = rows.pop()
        self.failUnlessEqual(row['id'], 23)
        self.failUnlessEqual(row['code'],
                             'ENERGY/NUCLEAR')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nComprehensive Energy Bill')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 22)
        self.failUnlessEqual(row['code'],
                             'TRANSPORTATION')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nH.R. 1495 Water Resources Development Act (WRDA) - the WRDA provisions to modernize the locks on the Upper Mississippi and Illinois Rivers are essential if U.S. agriculture is going to remain competitive in the global marketplace.\r\nH.R. 1495 the Water Resources Development Act of 2007 (WRDA) - conference report - Title VIII of the legislation includes authorization for the Corps of Engineers to construct new 1,200 foot locks on the Upper Mississippi and Illinois Rivers\n')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 21)
        self.failUnlessEqual(row['code'],
                             'IMMIGRATION')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nImmigration - Thanking Senator Lincoln and her staff for the hard work and long hours and dedication they presented in an effort to develop a comprehensive immigration reform.\n')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 20)
        self.failUnlessEqual(row['code'],
                             'AGRICULTURE')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nFY08 Agriculture Appropriations Bill - (Sec. 738) amendment to prohibit USDA from spending money for health inspection of horses.\n\nH.R. 3161, the FY08 Ag spending bill - amendments: King/Kingston amendment to strike Sec. 738. It would limit USDA authority for equine health inspection, effectively restricting the movement of all horses; Ackerman amendment prohibits funding for Food Safety and Inspection Service (FSIS) inspections in facilities that process nonambulatory or downer livestock;  Whitfield-Spratt-Rahall-Chandler amendment to restrict USDA inspection of horses intended for processing for human consumption.\n\nPayment Limits.\r\nFarm Bill: tax title, reductions in direct payments, counter-cyclical revenue option, senate ag committee markup on farm bill, amendments seeking further reform to payment limits and adjusted gross income restrictions.\n')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 19)
        self.failUnlessEqual(row['code'],
                             'TRADE (DOMESTIC/FOREIGN)')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nU.S. -Peru Trade Promotion Agreement (TPA) - the goal is to increase U.S. agriculture exports and increase market share.')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 18)
        self.failUnlessEqual(row['code'],
                             'EDUCATION')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nFY08 Labor, HHS and Education spending.  Perkins Amendment (federal funding for FFA and career and technical education).')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 17)
        self.failUnlessEqual(row['code'],
                             'ROADS/HIGHWAY')
        self.failUnlessEqual(row['specific_issue'],
                             '\r\nH.R. 3098 to restore farm truck exemptions from federal motor carrier vehicle regulations.')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 16)
        self.failUnlessEqual(row['code'],
                             'DEFENSE')
        self.failUnlessEqual(row['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\n')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 15)
        self.failUnlessEqual(row['code'],
                             'HOMELAND SECURITY')
        self.failUnlessEqual(row['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\nH.R.2638 & S.1644 FY08 DHS AppropriationsBill-CRP')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 14)
        self.failUnlessEqual(row['code'],
                             'BUDGET/APPROPRIATIONS')
        self.failUnlessEqual(row['specific_issue'],
                             'H.R.3222 & Senate FY08 Defense Appropriations-Navy, Army & SOCOM R&D\nH.R.1585 & S.1547 FY08 Defense Authorizations-Navy, Army & SOCOM R&D\nH.R.2638 & S.1644 FY08 DHS AppropriationsBill-CRP')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 13)
        self.failUnlessEqual(row['code'],
                             'DEFENSE')
        self.failUnlessEqual(row['specific_issue'],
                             'DEFENSE AUTHORIZATION, DEFENSE APPROPRIATIONS, VETERANS, DEFENSE HEALTH CARE, ARMED FORCES RETIREMENT, ARMED FORCES PERSONNEL BENEFITS, EMERGING DEFENSE RELATED ISSUES')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 12)
        self.failUnlessEqual(row['code'],
                             'BANKING')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 11)
        self.failUnlessEqual(row['code'],
                             'REAL ESTATE/LAND USE/CONSERVATION')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 10)
        self.failUnlessEqual(row['code'],
                             'FINANCIAL INSTITUTIONS/INVESTMENTS/SECURITIES')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 9)
        self.failUnlessEqual(row['code'],
                             'FOREIGN RELATIONS')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 8)
        self.failUnlessEqual(row['code'],
                             'LAW ENFORCEMENT/CRIME/CRIMINAL JUSTICE')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 7)
        self.failUnlessEqual(row['code'],
                             'FAMILY ISSUES/ABORTION/ADOPTION')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 6)
        self.failUnlessEqual(row['code'],
                             'HEALTH ISSUES')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 5)
        self.failUnlessEqual(row['code'],
                             'MEDICARE/MEDICAID')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 4)
        self.failUnlessEqual(row['code'],
                             'WELFARE')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 3)
        self.failUnlessEqual(row['code'],
                             'BUDGET/APPROPRIATIONS')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 2)
        self.failUnlessEqual(row['code'],
                             'TAXATION/INTERNAL REVENUE CODE')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        row = rows.pop()
        self.failUnlessEqual(row['id'], 1)
        self.failUnlessEqual(row['code'],
                             'INSURANCE')
        self.failUnlessEqual(row['specific_issue'],
                             'unspecified')

        self.failUnlessEqual(len(rows), 0)

    def test_import_issues_issue_code(self):
        """Importing issues should fill issue_code table."""
        filings = list(lobbyists.parse_filings(util.testpath('issues.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM issue_code")
        rows = list(cur)

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'ENERGY/NUCLEAR')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'TRANSPORTATION')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'IMMIGRATION')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'AGRICULTURE')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'TRADE (DOMESTIC/FOREIGN)')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'EDUCATION')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'ROADS/HIGHWAY')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'HOMELAND SECURITY')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'DEFENSE')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'BANKING')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'REAL ESTATE/LAND USE/CONSERVATION')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'FINANCIAL INSTITUTIONS/INVESTMENTS/SECURITIES')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'FOREIGN RELATIONS')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'LAW ENFORCEMENT/CRIME/CRIMINAL JUSTICE')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'FAMILY ISSUES/ABORTION/ADOPTION')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'HEALTH ISSUES')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'MEDICARE/MEDICAID')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'WELFARE')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'BUDGET/APPROPRIATIONS')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'TAXATION/INTERNAL REVENUE CODE')

        row = rows.pop()
        self.failUnlessEqual(row['code'],
                             'INSURANCE')

        self.failUnlessEqual(len(rows), 0)

    def test_import_filings_to_issues(self):
        """Issues are matched up with filings in the database."""
        filings = list(lobbyists.parse_filings(util.testpath('issues.xml')))
        con = sqlite3.connect(':memory:')
        con = lobbyists.create_db(con)
        cur = con.cursor()
        self.failUnless(lobbyists.import_filings(cur, filings))

        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM filing_issues")
        rows = list(cur)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 23)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 22)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 21)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 20)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 19)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 18)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '79E53F91-8C5F-44AD-909D-032AA25D5B00')
        self.failUnlessEqual(row['issue'], 17)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '05804BE5-57C9-41BF-97B2-0120826D4393')
        self.failUnlessEqual(row['issue'], 16)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '05804BE5-57C9-41BF-97B2-0120826D4393')
        self.failUnlessEqual(row['issue'], 15)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], '05804BE5-57C9-41BF-97B2-0120826D4393')
        self.failUnlessEqual(row['issue'], 14)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'F56492FC-4FBD-4824-83E1-0004B30F0519')
        self.failUnlessEqual(row['issue'], 13)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 12)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 11)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 10)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 9)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 8)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'A55002C7-78C4-41BA-A6CA-01FCF7650116')
        self.failUnlessEqual(row['issue'], 7)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 6)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 5)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 4)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 3)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 2)

        row = rows.pop()
        self.failUnlessEqual(row['filing'], 'D1C9DB2A-AE4F-4FED-9BCB-024C8373813E')
        self.failUnlessEqual(row['issue'], 1)

        self.failUnlessEqual(len(rows), 0)


if __name__ == '__main__':
    unittest.main()
    
