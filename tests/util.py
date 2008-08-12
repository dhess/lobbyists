#
# util.py - Test utilities.
# Copyright (C) 2008 Drew Hess <dhess@bothan.net>
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

"""Unit test utilities for lobbyists.py."""

import os.path

def testpath(basename):
    return os.path.join('tests', 'data', basename)

def ids_doc():
    return testpath('ids.xml')

def years_doc():
    return testpath('years.xml')

def filing_dates_doc():
    return testpath('filing_dates.xml')

def amounts_doc():
    return testpath('amounts.xml')

def periods_doc():
    return testpath('periods.xml')

def types_doc():
    return testpath('types.xml')
