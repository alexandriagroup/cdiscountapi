import os
import pytest
from unittest import skip
from ..cdiscountapi import Connection
from . import assert_response_succeeded, assert_response_failed


# TODO Find out how to get a not empty ParcelShopList
@pytest.mark.vcr()
def test_get_parcel_shop_list():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.relays.get_parcel_shop_list()
    assert_response_succeeded(response)
    assert response['ParcelShopList'] is None


@skip('Standby')
@pytest.mark.vcr()
def test_submit_relays_file():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.relays.submit_relays_file(
        relays_file_request={'RelaysFileURI': ''}
    )


@skip('Standby')
@pytest.mark.vcr()
def test_get_relays_file_submission_result():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.relays.get_relays_file_submission_result(
        relays_file_filter={'RelaysFileId': 1}
    )


@pytest.mark.vcr()
def test_get_relays_file_submission_result_without_relays_file():
    """
    With no relays file submitted, Relays.get_relays_file_submission_result
    should return an invalid response when any RelaysFileId is specified
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.relays.get_relays_file_submission_result(
        relays_file_filter={'RelaysFileId': 1}
    )
    assert_response_failed(response)
    assert response['RelaysFileIntegrationStatus'] is None
    assert response['RelaysLogList'] == {'RelayIntegrationLog': []}