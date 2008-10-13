all: help

help:
	@echo 'Choose one:'
	@echo
	@echo 'push - push to git origin remote.'
	@echo 'push-all - push to all git remotes.'
	@echo 'db - create (clobber) the filings.db database.'
	@echo 'test - run all unit tests.'
	@echo 'develop - run "setup.py develop".'
	@echo 'sdist - make a source distribution.'
	@echo 'egg - make a setuptools egg binary distribution.'
	@echo 'clean - remove build and dist subdirectories.'
	@echo 'help - this message.'

push:
	git push origin

push-all:
	git push --all

test:
	python setup.py test

db:
	sqlite3 lobbyists.db < lobbyists/lobbyists.sql

sdist:
	python setup.py sdist --formats=bztar

egg:
	python setup.py bdist_egg

develop:
	python setup.py develop

clean:
	rm -rf build dist
