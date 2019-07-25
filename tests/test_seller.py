# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import pytest
from . import assert_response_succeeded


@pytest.mark.vcr()
def test_get_seller_info(api):
    """
    get_seller_info should return the information about the seller
    """
    response = api.seller.get_seller_info()
    assert_response_succeeded(response)
    assert "Seller" in response


@pytest.mark.vcr()
def test_get_seller_indicators(api):
    """
    get_seller_indicators should return the performance indicators of the
    seller
    """
    response = api.seller.get_seller_indicators()
    assert_response_succeeded(response)
    assert "SellerIndicators" in response
