# -*- coding: utf-8 -*-
#
# test_doctests.py - Run any doctests in the package.
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

"""Run doctests."""

import unittest
import doctest
import util


suite = unittest.TestSuite()
for f in util.doc_file_tests():
    suite.addTest(doctest.DocFileSuite(f, module_relative=False))
runner = unittest.TextTestRunner()
runner.run(suite)
