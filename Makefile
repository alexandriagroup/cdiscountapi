SHELL := /bin/bash

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

test-no-vcr:
	VCR_RECORD_MODE=off py.test

test-renew-vcr-records:
	@rm -vfr $(ROOT_DIR)/cdiscountapi/tests/cassettes
	VCR_RECORD_MODE=once py.test
