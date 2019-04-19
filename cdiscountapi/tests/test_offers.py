# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from ..cdiscountapi import Connection
from . import assert_response_succeeded, CDISCOUNT_WITHOUT_DATA


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='timeout error unresolve by cdiscount')
@pytest.mark.vcr()
def test_get_offer_list(api):
    response = api.offers.get_offer_list()
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@pytest.mark.vcr()
def test_get_offer_list_paginated(api):
    response = api.offers.get_offer_list_paginated(PageNumber=2)
    assert_response_succeeded(response)
    assert 'OfferList' in response.keys()


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='submit_offer_package not ready')
@pytest.mark.vcr()
def test_submit_offer_package(api):
    response = api.offers.submit_offer_package()
    assert_response_succeeded(response)
    assert 'PackageId' in response.keys()


@pytest.mark.vcr()
def test_get_offer_package_submission_result(api):
    response = api.offers.get_offer_package_submission_result(541)
    assert_response_succeeded(response)
    assert 'OfferLogList' in response.keys()
