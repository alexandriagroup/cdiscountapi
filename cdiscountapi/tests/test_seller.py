# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import glob
import re
import requests
import pytest
from ..cdiscountapi import Connection
from ..exceptions import CdiscountApiTypeError


@pytest.mark.vcr()
def test_initialization():
    """
    The token and the header_message should be updated at initialization
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    assert re.match(r'[a-z0-9]{32}', api.token) is not None
    assert api.header == {
        'Context': {
            'SiteID': 100
        },
        'Localization': {
            'Country': 'Fr',
        },
        'Security': {
            'IssuerID': None,
            'SessionID': None,
            'TokenId': api.token,
            'UserName': '',
        },
        'Version': 1.0,
    }


@pytest.mark.vcr()
def test_token():
    """
    get_token should return the token
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    assert re.match(r'[a-z0-9]{32}', api.token) is not None


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
