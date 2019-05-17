# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import os
from shutil import rmtree
from tempfile import gettempdir
from copy import deepcopy

import pytest

from . import (
    CDISCOUNT_WITHOUT_DATA,
    assert_response_succeeded,
    assert_xml_files_equal
)
from ..sections.offers import Offers


@pytest.mark.skip(reason='timeout error unresolve by cdiscount')
@pytest.mark.vcr()
def test_get_offer_list(api):
    response = api.offers.get_offer_list()
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@pytest.mark.vcr()
def test_get_offer_list_paginated(api):
    response = api.offers.get_offer_list_paginated(PageNumber=2)
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@pytest.mark.vcr()
def test_generate_offer_package(valid_offer_package):
    output_dir = gettempdir()
    # Check uploading_package doesn't exists yet.
    assert 'uploading_package' not in os.listdir(output_dir)
    assert os.path.isfile(f'{output_dir}/uploading_package.zip') is False

    # Generate packages.
    # valid_offer_package contains 2 valid offers for the offer package
    Offers.generate_offer_package(output_dir, valid_offer_package)

    # Check uploading_package exists now.
    assert 'uploading_package' in os.listdir(output_dir)
    assert os.path.isfile(f'{output_dir}/uploading_package.zip') is True

    # Get expected Offers.xml.
    with open('cdiscountapi/tests/samples/offers/Offers.xml', 'r') as f:
        expected = f.read()

    # Get created Offers.xml.
    with open(f'{output_dir}/uploading_package/Content/Offers.xml', 'r') as f:
        created = f.read()

    # # Check Offers.xml is ok.
    # assert created == expected
    assert_xml_files_equal(
        created, expected,
        'Offer', expected_count=2,
    )


@pytest.mark.skip(reason='Standby')
# @pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='submit_offer_package not ready')
@pytest.mark.vcr()
def test_submit_offer_package(api):
    response = api.offers.submit_offer_package()
    assert_response_succeeded(response)
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_offer_package_submission_result(api):
    response = api.offers.get_offer_package_submission_result(541)
    assert_response_succeeded(response)
    assert 'OfferLogList' in response.keys()
