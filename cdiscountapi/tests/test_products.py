# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import json
import os
from unittest import skip

import pytest

from ..cdiscountapi import Connection

api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                 os.getenv('CDISCOUNT_API_PASSWORD'))


@pytest.mark.vcr()
def test_get_allowed_category_tree():
    response = api.products.get_allowed_category_tree()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'CategoryTree' in response.keys()


@pytest.mark.vcr()
def test_get_all_allowed_category_tree():
    response = api.products.get_all_allowed_category_tree()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'CategoryTree' in response.keys()


@pytest.mark.vcr()
def test_get_product_list():
    response = api.products.get_product_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductList' in response.keys()


@pytest.mark.vcr()
def test_get_model_list():
    response = api.products.get_model_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ModelList' in response.keys()


@skip('get_all_model_list not ready')
@pytest.mark.vcr()
def test_get_all_model_list():
    response = api.products.get_model_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ModelList' in response.keys()


@pytest.mark.vcr()
def test_get_brand_list():
    response = api.products.get_brand_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'BrandList' in response.keys()


@skip('submit_product_package not ready')
@pytest.mark.vcr()
def test_submit_product_package():
    with open('cdiscountapi/tests/samples/products/products_to_submit.json') as f:
        products_dict = json.loads(f.read())
    url = 'toto.html/'
    response = api.products.submit_product_package(products_dict, url)
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_product_package_submission_result():
    response = api.products.get_product_package_submission_result()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_product_package_product_matching_file_data():
    response = api.products.get_product_package_product_matching_file_data()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductMatchingList' in response.keys()


@pytest.mark.vcr()
def test_get_product_list_by_identifier():
    response = api.products.get_product_list_by_identifier()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductListByIdentifier' in response.keys()
