# -*- coding: utf-8 -*-
#
# test_normalize.py - Tests for the lobbyists module normalize
# function.
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

"""Tests for the lobbyists module normalize function."""

import unittest
import lobbyists
import util

class TestNormalize(unittest.TestCase):
    def test_normalize_filings(self):
        # The only optional attribute of a Filing element is Amount.
        # By default, normalize() sets unspecified amounts to None.
        filings = [lobbyists.normalize(x) for x in \
                       lobbyists.parse_filings(util.testpath('amounts.xml'))]

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'BAA88635-8674-4DF8-8825-2B0B3D8B4554') 
        self.failUnlessEqual(f['amount'], 108000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '9648F901-BA48-4EE5-BE8B-01D5551BFDA1') 
        self.failUnlessEqual(f['amount'], 20000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '8F21CC08-E136-4A42-A51D-25FE3B6CC303') 
        self.failUnlessEqual(f['amount'], 0)

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DE669D92-0620-4257-8B0C-01922EA0A226') 
        self.failUnlessEqual(f['amount'], None)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '5DA4C8F8-4E2D-4EE1-895C-00369A8222FB') 
        self.failUnlessEqual(f['amount'], None)

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DB4CCA2C-1E51-46A7-8800-00201697E905') 
        self.failUnlessEqual(f['amount'], None)

        self.failUnlessEqual(len(filings), 0)

    def test_normalize_filings2(self):
        # Convert unspecified amounts to 4999.
        filings = [lobbyists.normalize(x, exceptions={'amount': 4999}) \
                       for x in \
                       lobbyists.parse_filings(util.testpath('amounts.xml'))]

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'BAA88635-8674-4DF8-8825-2B0B3D8B4554') 
        self.failUnlessEqual(f['amount'], 108000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '9648F901-BA48-4EE5-BE8B-01D5551BFDA1') 
        self.failUnlessEqual(f['amount'], 20000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '8F21CC08-E136-4A42-A51D-25FE3B6CC303') 
        self.failUnlessEqual(f['amount'], 0)

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DE669D92-0620-4257-8B0C-01922EA0A226') 
        self.failUnlessEqual(f['amount'], 4999)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '5DA4C8F8-4E2D-4EE1-895C-00369A8222FB') 
        self.failUnlessEqual(f['amount'], 4999)

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DB4CCA2C-1E51-46A7-8800-00201697E905') 
        self.failUnlessEqual(f['amount'], 4999)

        self.failUnlessEqual(len(filings), 0)

    def test_normalize_filings3(self):
        # Convert unspecified amounts to 'unspecified'
        filings = [lobbyists.normalize(x, exceptions={}) for x in \
                       lobbyists.parse_filings(util.testpath('amounts.xml'))]

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'BAA88635-8674-4DF8-8825-2B0B3D8B4554') 
        self.failUnlessEqual(f['amount'], 108000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '9648F901-BA48-4EE5-BE8B-01D5551BFDA1') 
        self.failUnlessEqual(f['amount'], 20000)

        f = filings.pop()
        self.failUnlessEqual(f['id'], '8F21CC08-E136-4A42-A51D-25FE3B6CC303') 
        self.failUnlessEqual(f['amount'], 0)

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DE669D92-0620-4257-8B0C-01922EA0A226') 
        self.failUnlessEqual(f['amount'], 'unspecified')

        f = filings.pop()
        self.failUnlessEqual(f['id'], '5DA4C8F8-4E2D-4EE1-895C-00369A8222FB') 
        self.failUnlessEqual(f['amount'], 'unspecified')

        f = filings.pop()
        self.failUnlessEqual(f['id'], 'DB4CCA2C-1E51-46A7-8800-00201697E905') 
        self.failUnlessEqual(f['amount'], 'unspecified')

        self.failUnlessEqual(len(filings), 0)

if __name__ == '__main__':
    unittest.main()
