# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import pytest
from . import assert_response_succeeded, CDISCOUNT_WITHOUT_DATA


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
