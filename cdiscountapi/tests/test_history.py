import os
import pytest
from ..cdiscountapi import Connection


@pytest.mark.vcr()
def test_last_request_without_request():
    """
    When no request has been sent, Connection.last_request should return
    'No request sent.'
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    assert api.last_request == 'No request sent.'


@pytest.mark.vcr()
def test_last_request():
    """
    Connection.last_request should return the last SOAP request as a string
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    api.seller.get_seller_indicators()

    assert api.last_request.startswith(
        '<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">'
    )
    assert '<ns0:GetSellerIndicators xmlns:ns0="http://www.cdiscount.com">' in api.last_request
    assert api.last_request.endswith(
        '</soap-env:Envelope>\n'
    )


@pytest.mark.vcr()
def test_last_response_without_response():
    """
    When no response has been received, Connection.last_response should return
    'No response received.'
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    assert api.last_response == 'No response received.'


@pytest.mark.vcr()
def test_last_response():
    """
    Connection.last_response should return the last SOAP response as a string
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    api.seller.get_seller_indicators()

    assert api.last_response.startswith(
        '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
    )
    assert '<GetSellerIndicatorsResponse xmlns="http://www.cdiscount.com">' in api.last_response
    assert api.last_response.endswith(
        '</s:Envelope>\n'
    )
