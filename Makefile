SHELL := /bin/bash
PYTEST_FLAGS ?= --disable-pytest-warnings

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

install-dev:
	@echo "Installing the requirements for the development"
	pip install flit
	flit install --deps develop
	# Don't know why "pip install -e ." fails with: "No module named setuptools"
	# so I have to fallback to this command to install an "editable" version of
	# the package. (the package is actually the current directory. So every modification
	# is seen in the package installed. It's basically just a link to the current directory)
	python setup.py develop

docs:
	cd docs && make html && cd -

test:
	py.test $(PYTEST_FLAGS) --vcr-record=none

test-coverage:
	py.test $(PYTEST_FLAGS) --vcr-record=none --cov=cdiscountapi --cov-report term-missing

test-renew-vcr-records:
	py.test $(PYTEST_FLAGS) --vcr-record=all

build:
	flit build --format wheel

publish:
	git push origin master && flit publish --format wheel

.PHONY: docs test
