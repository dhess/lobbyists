all: help

help:
	@echo 'Choose one:'
	@echo
	@echo 'filings - create (clobber) the filings.db database.'
	@echo 'test - run unit tests.'
	@echo 'help - this message.'

test:
	PYTHONPATH=.:$$PYTHONPATH python tests/test_parse.py

filings:
	sqlite3 filings.db < filings.sql
