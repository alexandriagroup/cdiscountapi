# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from ..cdiscountapi import Connection


@pytest.mark.vcr()
def test_get_seller_info():
    """
    get_seller_info should return the information about the seller
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.seller.get_seller_info()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'Seller' in response


@pytest.mark.vcr()
def test_get_seller_indicators():
    """
    get_seller_indicators should return the performance indicators of the
    seller
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.seller.get_seller_indicators()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    assert response['OperationSuccess'] is True
    assert 'SellerIndicators' in response
