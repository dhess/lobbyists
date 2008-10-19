# -*- coding: utf-8 -*-
#
# test_parse_issues.py - Tests for lobbyists issue parsing.
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

"""Tests for lobbyists issue parsing."""

import unittest
import lobbyists
import util

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


if __name__ == '__main__':
    unittest.main()
