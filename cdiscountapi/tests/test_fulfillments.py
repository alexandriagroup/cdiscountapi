# -*- coding: utf-8 -*-
#
# Copyright © 2019 Alexandria

import os
import pytest
from . import assert_response_succeeded
from unittest import skip


@skip("submit not ready")
@pytest.mark.vcr()
def test_submit_fulfillment_supply_order(api):
    product_list = [
        {
            "ExternalSupplyOrderId": 12,
            "ProductEan": 1234567891234,
            "Quantity": 122,
            "SellerProductReference": 154,
            "Warehouse": "ANZ",
            "WarehouseReceptionMinDate": "2018-12-12",
        },
        {
            "ExternalSupplyOrderId": 13,
            "ProductEan": 1234567895234,
            "Quantity": 3,
            "SellerProductReference": 164,
            "Warehouse": "ANZ",
            "WarehouseReceptionMinDate": "2019-02-04",
        },
    ]

    response = api.fulfillment.submit_fulfillment_supply_order(product_list)
    assert_response_succeeded(response)
    assert "DepositId" in response.keys()


@pytest.mark.vcr()
def test_submit_fulfillment_supply_order_raises(api):
    product_list = [
        {
            "ExternalSupplyOrderId": 12,
            "ProductEan": 1234567891234,
            "Quantity": 122,
            "SellerProductReference": 154,
            "Toto": "ANZ",
            "WarehouseReceptionMinDate": "2018-12-12",
        },
        {
            "ExternalSupplyOrderId": 13,
            "ProductEan": 1234567895234,
            "Quantity": 3,
            "SellerProductReference": 164,
            "Warehouse": "ANZ",
            "WarehouseReceptionMinDate": "2019-02-04",
        },
    ]
    with pytest.raises(TypeError):
        api.fulfillment.submit_fulfillment_supply_order(product_list)


@skip("submit not ready")
@pytest.mark.vcr()
def test_submit_fulfillment_on_demand_supply_order(api):
    order_list = [
        {"OrderReference": "1703182124BNXCO", "ProductEan": "2009854780777"},
        {"OrderReference": "1852175648RHFTY", "ProductEan": "350075411599"},
    ]
    response = api.fulfillment.submit_fulfillment_on_demand_supply_order(order_list)
    assert_response_succeeded(response)
    assert "DepositId" in response.keys()


@pytest.mark.vcr()
def test_submit_fulfillment_on_demand_supply_order_raises(api):
    order_list = [
        {"OrderReference": "1703182124BNXCO", "ProductEan": "2009854780777"},
        {"OrderReference": "1852175648RHFTY", "Toto": "350075411599"},
    ]
    with pytest.raises(TypeError):
        api.fulfillment.submit_fulfillment_on_demand_supply_order(order_list)


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_fulfillment_supply_order_report_list(api):
    response = api.fulfillment.get_fulfillment_supply_order_report_list(PageSize=10)
    assert_response_succeeded(response)
    assert "ReportList" in response.keys()


@pytest.mark.vcr()
def test_get_fulfillment_supply_order_report_list_raises(api):
    with pytest.raises(TypeError):
        api.fulfillment.get_fulfillment_supply_order_report_list(Toto=10)


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_fulfillment_delivery_document(api):
    response = api.fulfillment.get_fulfillment_delivery_document(DepositId=233575)
    assert_response_succeeded(response)
    assert "ReportList" in response.keys()


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_fulfillment_supply_order(api):
    response = api.fulfillment.get_fulfillment_supply_order(PageNumber=1)
    assert_response_succeeded(response)
    assert "SupplyOrderLineList" in response.keys()


@skip("submit not ready")
@pytest.mark.vcr()
def test_submit_fulfillment_activation(api):
    product_list = [
        {
            "ProductActivationData": {
                "Action": "Activation",
                "Height": 1,
                "Length": 20,
                "ProductEan": "AX34567891234",
                "SellerProductReference": "ABVG45K",
                "Weight": 50,
                "Width": 10,
            }
        }
    ]
    req = api.factory.FulfilmentActivationRequest(product_list)
    response = api.fulfillment.submit_fulfillment_activation(req)
    assert_response_succeeded(response)
    assert "DepositId" in response.keys()


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_fulfillment_activation_report_list(api):
    response = api.fulfillment.get_fulfillment_activation_report_list(DepositIdList=10)
    assert_response_succeeded(response)
    assert "FulfilmentActivationReportList" in response.keys()


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_fulfillment_order_list_to_supply(api):
    response = api.fulfillment.get_fulfillment_order_list_to_supply(
        ProductEan=2009863600561
    )
    assert_response_succeeded(response)
    assert "FulfilmentActivationReportList" in response.keys()


@skip("submit not ready")
@pytest.mark.vcr()
def test_submit_offer_state_action(api):
    response = api.fulfillment.submit_offer_state_action(
        Action="Unpublish", SellerProductId=11504
    )
    assert_response_succeeded(response)


@skip("not authorized to access")
@pytest.mark.vcr()
def test_create_external_order(api):
    order_dict = {
        "Comments": None,
        "Corporation": "FNAC",
        "Customer": {
            "Civility": "M",
            "CustomerEmailAdress": "toto@mail.com",
            "CustomerFirstName": "Toto",
            "CustomerLastName": "Titi",
            "ShippingAdress": "19 rue Toto",
            "ShippingCity": "Toto",
            "ShippingCountry": "TOTO",
            "ShippingPostalCode": 00000,
        },
        "CustomerOrderNumber": "CDS2",
        "OrderDate": "2019-03-04-T01:01:01",
        "OrderLineList": {
            "ExternalOrderLine": {
                "ProductEan": "3401565611712",
                "ProductReference": None,
                "Quantity": 1,
            }
        },
        "ShippingMode": str,
    }
    response = api.fulfillment.create_external_order(order_dict)
    assert_response_succeeded(response)


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_external_order_status(api):
    response = api.fulfillment.get_external_order_status(
        Corporation="FNAC", CustomerOrderNumber="YLA_test_APIFBC_FODETP_20160414_02"
    )
    assert_response_succeeded(response)
    assert "Status" in response.keys()


@skip("not authorized to access")
@pytest.mark.vcr()
def test_get_product_stock_list(api):
    response = api.fulfillment.get_product_stock_list(
        BarCodeList=["3515450012475"], FulfilmentReferencement=None
    )
    assert_response_succeeded(response)
    assert "ProductStockList" in response.keys()
