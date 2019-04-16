import os
import pytest
import datetime
from ..cdiscountapi import Connection
from . import assert_response_succeeded, assert_response_failed, CDISCOUNT_WITHOUT_DATA
from ..config import REFUND_INFORMATION


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list()
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_by_state():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(States=['AcceptedBySeller', 'Shipped'])
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_by_date():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(
        BeginCreationDate=datetime.datetime(2077, 1, 1)
    )
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_corporation_code():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(
        CorporationCode='CDSB2C'
    )
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_order_type():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(
        OrderType='MKPFBC'
    )
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_order_numbers():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(
        PartnerOrderRef='X'
    )
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_fetch_parcels():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.get_order_list(
        FetchParcels=True, OrderReferenceList=['ORDER_NUMBER_1']
    )
    raise AssertionError


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


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_validate_order_list():
    """
    Orders.validate_order_list should validate the orders specified
    """
    raise AssertionError


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_create_refund_voucher():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    request = {
        'CommercialGestureList': {
            'Amount': 10,
            'MotiveId': 135
        },
        'OrderNumber': 'ORDER_NUMBER',
        'SellerRefundList': {
            'Mode': 'Claim',
            'Motive': 'VendorRejection',
            'RefundOrderLine': {
                'Ean': 'EAN',
                'RefundShippingCharges': True,
                'SellerProductId': 'SKU1'
            }
        }
    }
    response = api.orders.create_refund_voucher(**request)
    raise AssertionError


@pytest.mark.vcr()
def test_create_refund_voucher_with_invalid_data():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.create_refund_voucher()
    assert_response_failed(response)
    assert response['CommercialGestureList'] is None
    assert response['OrderNumber'] is None
    assert response['SellerRefundList'] is None


@pytest.mark.vcr()
def test_manage_parcel_without_argument():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.orders.manage_parcel()
    assert_response_failed(response)
    assert response['ParcelActionResultList'] is None


@pytest.mark.vcr()
def test_manage_parcel_with_nonexistent_order():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    parcel_actions_list = [
        {
            'ManageParcel': 'AskingForInvestigation',
            'ParcelNumber': 'PARCEL_NUMBER',
            'Sku': 'SKU',
         }
    ]
    response = api.orders.manage_parcel(
        parcel_actions_list=parcel_actions_list, scopus_id='SCOPUS_ID'
    )
    assert_response_failed(response)
    assert response['ParcelActionResultList'] is None
