# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import os
from shutil import rmtree
from tempfile import gettempdir
from copy import deepcopy
import zipfile
from pathlib import Path

import pytest

from . import (
    CDISCOUNT_WITHOUT_DATA,
    assert_response_succeeded,
    assert_xml_files_equal,
    discount_component,
    offer_publication_list
)
from ..sections.offers import Offers


# HELPERS
def assert_offer_package_is_valid(filename):
    z = zipfile.ZipFile(filename, 'r')
    files = set(z.namelist())
    expected_files = {'Content/Offers.xml', '_rels/.rels', '[Content_Types].xml'}
    assert files == expected_files


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
    # ---- BEFORE ----
    package_name = Path(gettempdir()) / 'uploading_package'
    zip_file = package_name.with_suffix('.zip')
    # Check uploading_package doesn't exists yet.
    assert not package_name.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    # valid_offer_package contains 2 valid offers for the offer package
    Offers.generate_offer_package(package_name, valid_offer_package)

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert package_name.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open('cdiscountapi/tests/samples/offers/Offers.xml', 'r') as f:
        expected = f.read()

    with open(f'{package_name}/Content/Offers.xml', 'r') as f:
        created = f.read()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, 'Offer')


@pytest.mark.vcr()
def test_generate_offer_package_with_discount(valid_offer_package):
    """
    When the key 'DiscountList' is in the offer for the package,
    Offers.generate_offer_package should generate the offer package with the
    node DiscountList in Offers.xml
    """
    # ---- BEFORE ----
    package_name = Path(gettempdir()) / 'uploading_package'
    zip_file = package_name.with_suffix('.zip')
    # Check uploading_package doesn't exists yet.
    assert not package_name.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    # We add the DiscountList in the first offer
    valid_offer_package[0]['DiscountList'] = {'DiscountComponent': [discount_component()]}
    Offers.generate_offer_package(package_name, valid_offer_package)

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert package_name.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open('cdiscountapi/tests/samples/offers/Offers_with_discount.xml', 'r') as f:
        expected = f.read()

    with open(f'{package_name}/Content/Offers.xml', 'r') as f:
        created = f.read()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, 'Offer')


@pytest.mark.vcr()
def test_generate_offer_package_with_offer_publication_list(valid_offer_package):
    """
    When the argument 'offer_publication_list' is specified,
    Offers.generate_offer_package should generate the offer package with the
    node OfferPublicationList in Offers.xml
    """
    # ---- BEFORE ----
    package_name = Path(gettempdir()) / 'uploading_package'
    zip_file = package_name.with_suffix('.zip')
    # Check uploading_package doesn't exists yet.
    assert not package_name.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    Offers.generate_offer_package(
        package_name, valid_offer_package,
        offer_publication_list=offer_publication_list())

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert package_name.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open('cdiscountapi/tests/samples/offers/Offers_with_offer_publication_list.xml', 'r') as f:
        expected = f.read()

    with open(f'{package_name}/Content/Offers.xml', 'r') as f:
        created = f.read()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, 'Offer')


@pytest.mark.vcr()
def test_generate_offer_package_with_purge_and_replace(valid_offer_package):
    """
    When the argument 'purge_and_replace' is set to True,
    Offers.generate_offer_package should should set the attribute
    PurgeAndReplace in the node OfferPackage to True in Offers.xml
    """
    # ---- BEFORE ----
    package_name = Path(gettempdir()) / 'uploading_package'
    zip_file = package_name.with_suffix('.zip')
    # Check uploading_package doesn't exists yet.
    assert not package_name.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    Offers.generate_offer_package(
        package_name, valid_offer_package,
        purge_and_replace=True)

    # ---- AFTER ----
    # Check uploading_package exists now.
    assert package_name.exists()
    assert zip_file.exists()
    assert_offer_package_is_valid(zip_file)

    with open('cdiscountapi/tests/samples/offers/Offers_with_purge_and_replace.xml', 'r') as f:
        expected = f.read()

    with open(f'{package_name}/Content/Offers.xml', 'r') as f:
        created = f.read()

    # Check Offers.xml is ok.
    assert_xml_files_equal(created, expected, 'Offer')
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
