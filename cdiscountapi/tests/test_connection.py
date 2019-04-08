# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria


import os
import re
import pytest
from ..cdiscountapi import Connection
from ..exceptions import CdiscountApiConnectionError


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
            'SiteID': 100,
            'CatalogID': 1
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
    assert api.preprod is False


@pytest.mark.vcr()
def test_initialization_with_invalid_credentials():
    """
    Connection should raise a CdiscountApiConnectionError when
    the credentials are invalid
    """
    pytest.raises(CdiscountApiConnectionError, Connection, None,
                  os.getenv('CDISCOUNT_API_PASSWORD'))

    pytest.raises(CdiscountApiConnectionError, Connection,
                  os.getenv('CDISCOUNT_API_LOGIN'), None)


@pytest.mark.vcr()
def test_token():
    """
    get_token should return the token
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    assert re.match(r'[a-z0-9]{32}', api.token) is not None
