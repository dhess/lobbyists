#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

version = __import__('lobbyists').VERSION

setup(
    name = 'lobbyists',
    version = version,
    packages = ['lobbyists'],
    test_suite = 'lobbyists',

    package_data = { 'lobbyists' : ['lobbyists.sql'] },
    entry_points = {
        'console_scripts': ['lobbyists-load = lobbyists.util:load_main',
                            'lobbyists-benchmark = lobbyists.benchmark:main']
        },
    
    author = 'Drew Hess',
    author_email = 'dhess-src@bothan.net',
    description = 'Parse Senate LD-1/LD-2 lobbying disclosure XML documents',
    license = 'AGPLv3',
    keywords = 'lobbyists government parser',
    url = 'http://github.com/dhess/lobbyists/',
    long_description = """
This package provides a reference parser and database importer for the
United States Senate LD-1/LD-2 lobbying disclosure database. The
Senate provides the database as a series of XML documents,
downloadable here:

http://www.senate.gov/legislative/Public_Disclosure/database_download.htm

The SQL database schema used by the importer is a direct translation
of the XML schema used in the Senate documents. This isn't a
particularly useful format for analyzing lobbying data, but it is
useful for analyzing the lobbying records themselves, which often
contain errors or anomalies. In any case, it shouldn't be too
difficult to adapt the importing code in this package to a more useful
schema.
""",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
    )
