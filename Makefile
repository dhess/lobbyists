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
	@echo 'deb - make a Debian package.'
	@echo 'pypi - upload the package to PyPI.'
	@echo 'clean - remove build and dist subdirectories.'
	@echo 'help - this message.'

push:
	git push origin

push-all: push
	git push github

test:
	python setup.py test

db:
	sqlite3 lobbyists.db < lobbyists/lobbyists.sql

sdist:
	COPYFILE_DISABLE=true python setup.py sdist --formats=bztar

egg:
	python setup.py bdist_egg

deb:
	debuild -i\.git -I\.git

develop:
	python setup.py develop

pypi:
	COPYFILE_DISABLE=true python setup.py sdist bdist_egg upload --sign

clean:
	rm -rf build dist
