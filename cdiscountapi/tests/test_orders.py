import os
import pytest
from ..cdiscountapi import Connection
from unittest import skip
from . import assert_response_succeeded


@skip('Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list():
    pass


@pytest.mark.vcr()
def test_get_order_list_without_orders():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list()
    assert_response_succeeded(response)
    # OrderList should be None
    assert response['OrderList'] is None


@pytest.mark.vcr()
def test_get_global_configuration():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_global_configuration()
    assert_response_succeeded(response)
    # CarrierList should not be None
    assert response['CarrierList'] is not None


@pytest.mark.vcr()
def test_prepare_validations():
    """
    Orders.prepare_validations should return a valid dictionary that will be
    used in Orders.validate_order_list
    """
    order1 = {
        'CarrierName': 'CARRIER_NAME1',
        'OrderNumber': 'ORDER_NUMBER1',
        'OrderState': 'AcceptedBySeller',
        'TrackingNumber': 'TRACKING_NUMBER1',
        'TrackingUrl': 'TRACKING_URL1',
        'OrderLineList': [
            {'AcceptationState': 'AcceptedBySeller', 'SellerProductId': 'SKU1'},
            {'AcceptationState': 'RefusedBySeller', 'SellerProductId': 'SKU2'}
        ]
    }

    order2 = {
        'CarrierName': 'CARRIER_NAME2',
        'OrderNumber': 'ORDER_NUMBER2',
        'OrderState': 'RefusedBySeller',
        'TrackingNumber': 'TRACKING_NUMBER2',
        'TrackingUrl': 'TRACKING_URL2',
        'OrderLineList': [
            {'AcceptationState': 'RefusedBySeller', 'SellerProductId': 'SKU3'},
        ]
    }

    expected = {'OrderList':
    {'ValidateOrder':
        [{'CarrierName': 'CARRIER_NAME1',
            'OrderNumber': 'ORDER_NUMBER1',
            'OrderState': 'AcceptedBySeller',
            'TrackingNumber': 'TRACKING_NUMBER1',
            'TrackingUrl': 'TRACKING_URL1',
            'OrderLineList': {
                'ValidateOrderLine': [{'AcceptationState': 'AcceptedBySeller',
                    'ProductCondition': None,
                    'SellerProductId': 'SKU1',
                    'TypeOfReturn': None},
                    {'AcceptationState': 'RefusedBySeller',
                        'ProductCondition': None,
                        'SellerProductId': 'SKU2',
                        'TypeOfReturn': None}]},
        },
        {'CarrierName': 'CARRIER_NAME2',
            'OrderNumber': 'ORDER_NUMBER2',
            'OrderState': 'RefusedBySeller',
            'TrackingNumber': 'TRACKING_NUMBER2',
            'TrackingUrl': 'TRACKING_URL2',
            'OrderLineList': {
                'ValidateOrderLine': [{'AcceptationState': 'RefusedBySeller',
                    'ProductCondition': None,
                    'SellerProductId': 'SKU3',
                    'TypeOfReturn': None}]},
        }]}}

    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    assert api.orders.prepare_validations([order1, order2]) == expected



