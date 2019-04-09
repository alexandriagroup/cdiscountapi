import os
import pytest
from ..cdiscountapi import Connection
from . import assert_response_succeeded
from unittest import skip

api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                 os.getenv('CDISCOUNT_API_PASSWORD'))


@skip('timeout error unresolve by cdiscount')
@pytest.mark.vcr()
def test_get_offer_list():
    response = api.offers.get_offer_list()
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@pytest.mark.vcr()
def test_get_offer_list_paginated():
    pn = {'PageNumber': 1}
    response = api.offers.get_offer_list_paginated(pn)
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@skip('submit_offer_package not ready')
@pytest.mark.vcr()
def test_submit_offer_package():
    response = api.offers.submit_offer_package()
    assert_response_succeeded(response)
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_offer_package_submission_result():
    packages = {'PackageID': 541}
    response = api.offers.get_offer_package_submission_result(packages)
    assert_response_succeeded(response)
    assert 'OfferLogList' in response.keys()
