# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import os
from shutil import rmtree
from tempfile import gettempdir

import pytest

from . import (
    CDISCOUNT_WITHOUT_DATA,
    assert_response_succeeded,
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


@pytest.mark.skip(reason='Stand by')
@pytest.mark.vcr()
def test_generate_product_package():
    path = gettempdir()
    # Check uploading_package doesn't exists yet.
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False

    # Get product_dict from json file.
    filename = 'cdiscountapi/tests/samples/products/products_to_submit.json'
    with open(filename, 'r') as f:
        product_dict = json.load(f)

    # Generate packages.
    Products.generate_product_package(path, product_dict)

    # Check uploading_package exists now.
    assert 'uploading_package' in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is True

    # Get expected Products.xml.
    filename = 'cdiscountapi/tests/samples/products/Products.xml'
    with open(filename, 'r') as f:
        expected = f.read()

    # Get created Products.xml.
    filename = f'{path}/uploading_package/Content/Products.xml'
    with open(filename, 'r') as f:
        created = f.read()

    # Check Products.xml is ok.
    assert created == expected

    # Remove temporary files.
    rmtree(f'{path}/uploading_package')
    os.remove(f'{path}/uploading_package.zip')
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='submit_product_package not ready')
@pytest.mark.vcr()
def test_submit_product_package(api):
    with open('cdiscountapi/tests/samples/products/products_to_submit.json') as f:
        products_dict = json.loads(f.read())
    url = 'toto.html/'
    response = api.products.submit_product_package(products_dict, url)
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
