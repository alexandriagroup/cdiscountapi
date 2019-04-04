# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from ..cdiscountapi import Connection


@pytest.mark.vcr()
def test_get_allowed_category_tree():
    pass


@pytest.mark.vcr()
def test_get_all_allowed_category_tree():
    pass


@pytest.mark.vcr()
def test_get_model_list():
    """
    get_product_list should return the information about products
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.products.get_model_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'ModelList' in response


@pytest.mark.vcr()
def test_get_all_model_list():
    pass


@pytest.mark.vcr()
def test_get_brand_list():
    pass


@pytest.mark.vcr()
def test_submit_product_package():
    pass


@pytest.mark.vcr()
def test_get_product_package_submission_result():
    pass


@pytest.mark.vcr()
def test_get_product_package_product_matching_file_data():
    pass


@pytest.mark.vcr()
def test_get_product_list_by_identifier():
    pass



