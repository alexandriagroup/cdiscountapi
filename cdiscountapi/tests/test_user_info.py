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


def read_fixture(filename):
    with open('cdiscountapi/tests/samples/{}'.format(filename),
              'r', encoding='utf8') as f:
        return f.read()


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


# def test_get_user_info_type_none():
    # api = Connection(token='BestToken')
    # with pytest.raises(CdiscountApiTypeError):
    #     api.get_seller_info(user_id=None)


# # def test_get_user_info_bad_response():
# #     with Mocker() as m:
# #         api_response = read_fixture("seller_info_bad_request.xml")
# #         m.get(WSDL_URL, text=api_response)
# #         api = Connection(token='BestToken')
# #         result = api.get_seller_info()
# #         assert result is None
