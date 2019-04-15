SHELL := /bin/bash
PYTEST_FLAGS ?= --disable-pytest-warnings

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

install-dev:
	@echo "Installing the requirements for the development"
	pip install flit
	flit install --deps develop

test:
	py.test $(PYTEST_FLAGS) --vcr-record=none

test-coverage:
	py.test $(PYTEST_FLAGS) --vcr-record=none --cov=cdiscountapi --cov-report term-missing

test-renew-vcr-records:
	py.test $(PYTEST_FLAGS) --vcr-record=all
