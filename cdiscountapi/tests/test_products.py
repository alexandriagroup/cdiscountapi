# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import os
from shutil import rmtree
from tempfile import gettempdir, NamedTemporaryFile
from pathlib import Path
import zipfile

import pytest

from . import (
    CDISCOUNT_WITHOUT_DATA,
    assert_response_succeeded,
    assert_xml_files_equal,
)
from ..sections.products import Products


@pytest.mark.vcr()
def test_get_allowed_category_tree(api):
    response = api.products.get_allowed_category_tree()
    assert_response_succeeded(response)
    assert 'CategoryTree' in response.keys()


@pytest.mark.vcr()
def test_get_product_list(api):
    response = api.products.get_product_list('06010201')
    assert_response_succeeded(response)
    assert 'ProductList' in response.keys()


@pytest.mark.vcr()
def test_get_product_list_empty(api):
    with pytest.raises(TypeError):
        api.products.get_product_list()


@pytest.mark.vcr()
def test_get_model_list(api):
    response = api.products.get_model_list()
    assert_response_succeeded(response)
    assert 'ModelList' in response.keys()


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='get_all_model_list not ready')
@pytest.mark.vcr()
def test_get_all_model_list(api):
    response = api.products.get_model_list()
    assert_response_succeeded(response)
    assert 'ModelList' in response.keys()


@pytest.mark.vcr()
def test_get_brand_list(api):
    response = api.products.get_brand_list()
    assert_response_succeeded(response)
    assert 'BrandList' in response.keys()


# @pytest.mark.skip(reason='Stand by')
@pytest.mark.vcr()
def test_generate_product_package(valid_product_package):
    # ---- BEFORE ----
    package_name = Path(gettempdir()) / 'uploading_package'
    zip_file = package_name.with_suffix('.zip')
    # Check uploading_package doesn't exists yet.
    assert not package_name.exists()
    assert not zip_file.exists()

    # ---- PROCESS ----
    # Generate packages.
    Products.generate_product_package(package_name, valid_product_package)

    # ---- AFTER ----
    # Check uploading_package.zip exists now.
    assert not package_name.exists()
    assert zip_file.exists()

    # Get expected Products.xml.
    filename = 'cdiscountapi/tests/samples/products/Products.xml'
    with open(filename, 'r') as f:
        expected = f.read()

    with zipfile.ZipFile(zip_file) as zf:
        created = zf.read('Content/Products.xml').decode()

    # Check Products.xml is ok.
    assert_xml_files_equal(created, expected, 'Product')


def test_generate_product_package_with_nonexistent_directory(valid_product_for_package):
    """
    When the parent of the package_name does not exist a FileNotFoundError
    Products.generate_product_package should raise a FileNotFoundError
    """
    package_name = '/nonexistent/dir/uploading_package'
    pytest.raises(FileNotFoundError, Products.generate_product_package,
                  package_name, valid_product_for_package)


def test_generate_product_package_with_existing_package_name(valid_product_for_package):
    """
    When the package_name already exists Products.generate_product_package should
    raise a FileExistsError
    """
    with NamedTemporaryFile() as tmp_file:
        pytest.raises(FileExistsError, Products.generate_product_package,
                      tmp_file.name, valid_product_for_package)


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='submit_product_package not ready')
@pytest.mark.vcr()
def test_submit_product_package(api):
    url = 'https://www.myserver/uploading_package.zip'
    response = api.products.submit_product_package(url)
    assert_response_succeeded(response)
    assert 'PackageId' in response.keys()


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='to test after a submission')
@pytest.mark.vcr()
def test_get_product_package_submission_result(api):
    response = api.products.get_product_package_submission_result()
    assert_response_succeeded(response)
    assert 'PackageId' in response.keys()


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='to test with a correct package id')
@pytest.mark.vcr()
def test_get_product_package_product_matching_file_data(api):
    response = api.products.get_product_package_product_matching_file_data()
    assert_response_succeeded(response)
    assert 'ProductMatchingList' in response.keys()


@pytest.mark.vcr()
def test_get_product_list_by_identifier(api):
    response = api.products.get_product_list_by_identifier(['7426775682419'])
    assert_response_succeeded(response)
    assert 'ProductListByIdentifier' in response.keys()
