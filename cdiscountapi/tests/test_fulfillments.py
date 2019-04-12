# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from ..cdiscountapi import Connection
from . import assert_response_succeeded
from unittest import skip

api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                 os.getenv('CDISCOUNT_API_PASSWORD'))


@skip('submit not ready')
@pytest.mark.vcr()
def test_submit_fulfillment_supply_order():
    response = api.fulfillment.submit_fulfillment_supply_order()
    assert_response_succeeded(response)
    assert 'DepositId' in response.keys()


@skip('submit not ready')
@pytest.mark.vcr()
def test_submit_fulfillment_on_demand_supply_order():
    response = api.fulfillment.submit_fulfillment_on_demand_supply_order()
    assert_response_succeeded(response)
    assert 'DepositId' in response.keys()


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_fulfillment_supply_order_report_list():
    response = api.fulfillment.get_fulfillment_supply_order_report_list(PageSize=10)
    assert_response_succeeded(response)
    assert 'ReportList' in response.keys()


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_fulfillment_delivery_document():
    response = api.fulfillment.get_fulfillment_delivery_document(DepositId=233575)
    assert_response_succeeded(response)
    assert 'ReportList' in response.keys()




