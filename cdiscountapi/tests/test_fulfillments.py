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
    product_list = [
        {
            'ExternalSupplyOrderId': 12,
            'ProductEan': 1234567891234,
            'Quantity': 122,
            'SellerProductReference': 154,
            'Warehouse': 'ANZ',
            'WarehouseReceptionMinDate': '2018-12-12'
        },
        {
            'ExternalSupplyOrderId': 13,
            'ProductEan': 1234567895234,
            'Quantity': 3,
            'SellerProductReference': 164,
            'Warehouse': 'ANZ',
            'WarehouseReceptionMinDate': '2019-02-04'
        },
    ]

    response = api.fulfillment.submit_fulfillment_supply_order(product_list)
    assert_response_succeeded(response)
    assert 'DepositId' in response.keys()


@pytest.mark.vcr()
def test_submit_fulfillment_supply_order_raises():
    product_list = [
        {
            'ExternalSupplyOrderId': 12,
            'ProductEan': 1234567891234,
            'Quantity': 122,
            'SellerProductReference': 154,
            'Toto': 'ANZ',
            'WarehouseReceptionMinDate': '2018-12-12'
        },
        {
            'ExternalSupplyOrderId': 13,
            'ProductEan': 1234567895234,
            'Quantity': 3,
            'SellerProductReference': 164,
            'Warehouse': 'ANZ',
            'WarehouseReceptionMinDate': '2019-02-04'
        },
    ]
    with pytest.raises(ValueError):
        api.fulfillment.submit_fulfillment_supply_order(product_list)


@skip('submit not ready')
@pytest.mark.vcr()
def test_submit_fulfillment_on_demand_supply_order():
    order_list = [
        {
            'OrderReference': '1703182124BNXCO',
            'ProductEan': '2009854780777'
        },
        {
            'OrderReference': '1852175648RHFTY',
            'ProductEan': '350075411599'
         }
    ]
    response = api.fulfillment.submit_fulfillment_on_demand_supply_order(order_list)
    assert_response_succeeded(response)
    assert 'DepositId' in response.keys()


@pytest.mark.vcr()
def test_submit_fulfillment_on_demand_supply_order_raises():
    order_list = [
        {
            'OrderReference': '1703182124BNXCO',
            'ProductEan': '2009854780777'
        },
        {
            'OrderReference': '1852175648RHFTY',
            'Toto': '350075411599'
         }
    ]
    with pytest.raises(ValueError):
        api.fulfillment.submit_fulfillment_on_demand_supply_order(order_list)


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


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_fulfillment_supply_order():
    response = api.fulfillment.get_fulfillment_supply_order(PageNumber=1)
    assert_response_succeeded(response)
    assert 'SupplyOrderLineList' in response.keys()


@skip('submit not ready')
@pytest.mark.vcr()
def test_submit_fulfillment_activation():
    response = api.fulfillment.submit_fulfillment_activation()
    assert_response_succeeded(response)
    assert 'DepositId' in response.keys()


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_fulfillment_activation_report_list():
    response = api.fulfillment.get_fulfillment_activation_report_list()
    assert_response_succeeded(response)
    assert 'FulfilmentActivationReportList' in response.keys()


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_fulfillment_order_list_to_supply():
    response = api.fulfillment.get_fulfillment_order_list_to_supply()
    assert_response_succeeded(response)
    assert 'FulfilmentActivationReportList' in response.keys()


@skip('submit not ready')
@pytest.mark.vcr()
def test_submit_offer_state_action():
    response = api.fulfillment.submit_offer_state_action(
        Action='Unpublish',
        SellerProductId=11504
    )
    assert_response_succeeded(response)


@skip('not authorized to access')
@pytest.mark.vcr()
def test_create_external_order():
    response = api.fulfillment.create_external_order()
    assert_response_succeeded(response)


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_external_order_status():
    response = api.fulfillment.get_external_order_status(
        Corporation='FNAC',
        CustomerOrderNumber='YLA_test_APIFBC_FODETP_20160414_02'
    )
    assert_response_succeeded(response)
    assert 'Status' in response.keys()


@skip('not authorized to access')
@pytest.mark.vcr()
def test_get_product_stock_list():
    response = api.fulfillment.get_product_stock_list(
        BarCodeList=['3515450012475'],
        FulfilmentReferencement=None
    )
    assert_response_succeeded(response)
    assert 'ProductStockList' in response.keys()
