# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from ..cdiscountapi import Connection


@pytest.mark.vcr()
def test_get_allowed_category_tree():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_allowed_category_tree()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'CategoryTree' in response.keys()


@pytest.mark.vcr()
def test_get_all_allowed_category_tree():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_all_allowed_category_tree()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'CategoryTree' in response.keys()


@pytest.mark.vcr()
def test_get_product_list():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_product_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductList' in response.keys()


@pytest.mark.vcr()
def test_get_model_list():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_model_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ModelList' in response.keys()


# @pytest.mark.vcr()
# def test_get_all_model_list():
#     api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
#                      os.getenv('CDISCOUNT_API_PASSWORD'))
#     response = api.products.get_model_list()
#     assert response['ErrorList'] is None
#     assert response['ErrorMessage'] is None
#     assert response['OperationSuccess'] is True
#     assert 'ModelList' in response.keys()


@pytest.mark.vcr()
def test_get_brand_list():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_brand_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'BrandList' in response.keys()


@pytest.mark.vcr()
def test_submit_product_package():
    pass


@pytest.mark.vcr()
def test_get_product_package_submission_result():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_product_package_submission_result()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_product_package_product_matching_file_data():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_product_package_product_matching_file_data()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductMatchingList' in response.keys()


@pytest.mark.vcr()
def test_get_product_list_by_identifier():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_product_list_by_identifier()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ProductListByIdentifier' in response.keys()



