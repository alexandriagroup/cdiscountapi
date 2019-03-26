# -*- coding: utf-8 -*-
# 
# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

from requests_mock import Mocker
import pytest
from ..cdiscountapi import CdiscountApi
from ..exceptions import CdiscountApiTypeError


def test_get_seller_info():
    """Test get_user_info  with a mock."""

    expected_response = open("cdiscountapi/tests/samples/get_seller_info", "r", encoding='utf8').read()
    api = CdiscountApi(credentials={
        'wsdl': 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl',
        'token': 'thetoken',
        'login': 'thebestlogin'
    })
    response = api.get_seller_info()

    assert response == expected_response


def test_get_user_info_type_none():
    api = CdiscountApi({
        'wsdl': 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl',
        'token': 'thetoken',
        'login': 'thebestlogin'
    })
    with pytest.raises(CdiscountApiTypeError):
        api.get_seller_info(user_id=None)


def test_get_user_info_bad_response():
    with Mocker() as m:
        api_response = open("cdiscountapi/tests/samples/seller_info_bad_request", "r", encoding='utf8').read()
        m.get('https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl', text=api_response)
        api = CdiscountApi(credentials={
            'wsdl': 'https://wsvc.cdiscount.com/MarketplaceAPIService.svc?wsdl',
            'token': 'thetoken',
            'login': 'thebestlogin'
        })
        result = api.get_seller_info()
        assert result is None
