# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria


import os
import re
import pytest
from ..cdiscountapi import Connection

from ..exceptions import CdiscountApiConnectionError


# HELPER FUNCTION
def assert_header_message_is_correct(header, token):
    assert header["Version"] == "1.0"
    assert header["Security"] == {
        "DomainRightsList": None,
        "IssuerID": None,
        "SessionID": None,
        "SubjectLocality": None,
        "TokenId": token,
        "UserName": "",
    }
    assert header["Context"] == {
        "CatalogID": 1,
        "ConfigurationPolicy": None,
        "CustomerID": None,
        "CustomerId": None,
        "CustomerNumber": None,
        "CustomerPoolID": None,
        "GeoCoordinate": None,
        "SecuredContext": None,
        "SiteID": 100,
    }
    assert header["Localization"] == {
        "Country": "Fr",
        "CultureName": None,
        "Currency": "Eur",
        "DecimalPosition": 2,
        "Language": None,
    }


@pytest.mark.vcr()
def test_initialization():
    """
    The token and the header_message should be updated at initialization
    """
    api = Connection(
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        config="cdiscountapi/tests/samples/config.yaml",
    )
    assert re.match(r"[a-z0-9]{32}", api.token) is not None
    assert api.preprod is False
    assert_header_message_is_correct(api.header, api.token)


@pytest.mark.vcr()
def test_initialization_with_invalid_credentials():
    """
    Connection should raise a CdiscountApiConnectionError when
    the credentials are invalid
    """
    pytest.raises(
        CdiscountApiConnectionError,
        Connection,
        None,
        os.getenv("CDISCOUNT_API_PASSWORD"),
    )

    pytest.raises(
        CdiscountApiConnectionError, Connection, os.getenv("CDISCOUNT_API_LOGIN"), None
    )


@pytest.mark.vcr()
def test_header_message_with_config():
    """
    Connection.header should have the values specified in the config file when
    a config file is provided in the constructor
    """
    api = Connection(
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        config="cdiscountapi/tests/samples/config.yaml",
    )

    assert set(api.header.keys()) == {"Version", "Security", "Context", "Localization"}
    assert_header_message_is_correct(api.header, api.token)


@pytest.mark.vcr()
def test_header_message_with_nonexistent_config():
    """
    A CdiscountApiConnectionError should be raised when the
    config file specified in the constructor does not exist
    """
    pytest.raises(
        CdiscountApiConnectionError,
        Connection,
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        config="nonexistent_file",
    )


@pytest.mark.vcr()
def test_header_message_with_variable():
    """
    Connection.header should have the values specified in the header_message
    variable when the variable is provided in the constructor
    """
    header_message = {
        "Context": {"SiteID": 100, "CatalogID": 1},
        "Localization": {"Country": "Fr"},
        "Security": {"UserName": ""},
        "Version": "1.0",
    }

    api = Connection(
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        header_message=header_message,
    )

    # The speficied values should be set in the header and the missing fields
    # should have the value None
    assert api.header == {
        "Context": {
            "CatalogID": header_message["Context"]["CatalogID"],
            "ConfigurationPolicy": None,
            "CustomerID": None,
            "CustomerId": None,
            "CustomerNumber": None,
            "CustomerPoolID": None,
            "GeoCoordinate": None,
            "SecuredContext": None,
            "SiteID": header_message["Context"]["SiteID"],
        },
        "Localization": {
            "Country": header_message["Localization"]["Country"],
            "CultureName": None,
            "Currency": None,
            "DecimalPosition": None,
            "Language": None,
        },
        "Security": {
            "DomainRightsList": None,
            "IssuerID": None,
            "SessionID": None,
            "SubjectLocality": None,
            "TokenId": api.token,
            "UserName": header_message["Security"]["UserName"],
        },
        "Version": header_message["Version"],
    }


@pytest.mark.vcr()
def test_header_message_with_both_config_and_header_message():
    """
    A CdiscountApiConnectionError should be raised when both
    config and header_message are specified in the constructor
    """
    pytest.raises(
        CdiscountApiConnectionError,
        Connection,
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        config="any_config",
        header_message={"Context": {"SiteID": 100, "CatalogID": 1}},
    )
