SHELL := /bin/bash
PYTEST_FLAGS := --disable-pytest-warnings

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

install-dev:
	@echo "Installing the requirements for the development"
	pip install -r requirements-dev.txt

test:
	VCR_RECORD_MODE=off py.test $(PYTEST_FLAGS)

test-coverage:
	VCR_RECORD_MODE=off py.test $(PYTEST_FLAGS) --cov=cdiscountapi --cov-report term-missing

test-renew-vcr-records:
	@rm -vfr $(ROOT_DIR)/cdiscountapi/tests/cassettes
	VCR_RECORD_MODE=once py.test
