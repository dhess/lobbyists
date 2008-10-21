#
# util.py - Test utilities.
# Copyright (C) 2008 Drew Hess <dhess@bothan.net>
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

"""Unit test utilities for lobbyists.py."""

import os.path


def testpath(basename):
    try:
        # if packaged as a setuptools egg.
        from pkg_resources import resource_string
        return resource_string(__name__, basename)
    except:
        return os.path.join(os.path.dirname(__file__), 'data', basename)


def flatten(lst):
    result = list()
    for x in lst:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result


def doc_file_tests():
    """Return a sequence of non-Python files containing doctests."""
    try:
        # if packaged as a setuptools egg.
        from pkg_resources import resource_string
        yield resource_string(__name__, 'HOWTO.txt')
    except:
        yield os.path.join(os.path.dirname(__file__),
                            '../../doc', 'HOWTO.txt')
