import pytest
import datetime
from . import assert_response_succeeded, assert_response_failed, CDISCOUNT_WITHOUT_DATA


@pytest.fixture
def refund_voucher_request():
    return {
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


# get_order_list {{{1
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list(api):
    response = api.orders.get_order_list()
    assert_response_succeeded(response)
    assert response['OrderList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_by_state_with_orders_waiting_to_be_accepted(api):
    response = api.orders.get_order_list(States=['ShipmentRefusedBySeller'])
    assert_response_succeeded(response)
    assert response['OrderList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_by_date(api):
    response = api.orders.get_order_list(
        BeginCreationDate=datetime.datetime(2019, 4, 24),
        States=['ShipmentRefusedBySeller']
    )
    assert_response_succeeded(response)
    assert response['OrderList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_by_date_with_no_order_at_date(api):
    response = api.orders.get_order_list(
        BeginCreationDate=datetime.datetime(2077, 1, 1),
        States=['ShipmentRefusedBySeller']
    )
    assert_response_succeeded(response)
    assert response['OrderList'] is None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_corporation_code(api):
    response = api.orders.get_order_list(
        CorporationCode='CDSB2C'
    )
    assert_response_succeeded(response)
    assert response['OrderList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_order_type(api):
    response = api.orders.get_order_list(
        OrderType='None'
    )
    assert_response_succeeded(response)
    assert response['OrderList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_get_order_list_with_order_numbers(api):
    response = api.orders.get_order_list(
        OrderReferenceList=['ORDER_NUMBER_1', '1904240959CN8HI', 'ORDER_NUMBER_2']
    )
    assert_response_succeeded(response)

    # Only 1904240959CN8HI is an existing order number
    assert len(response['OrderList']['Order']) == 1


# get_global_configuration {{{1
@pytest.mark.vcr()
def test_get_global_configuration(api):
    response = api.orders.get_global_configuration()
    assert_response_succeeded(response)
    # CarrierList should not be None
    assert response['CarrierList'] is not None


# prepare_validations {{{1
@pytest.mark.vcr()
def test_prepare_validations(api):
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
    assert api.orders.prepare_validations([order1, order2]) == expected


# validate_order_list {{{1
# Difficult to test validate_order_list with vcr, as the action must be
# run at least once, which will change the state of the order that won't be
# allowed to change the next run.
@pytest.mark.skip
@pytest.mark.vcr()
def test_validate_order_list(api):
    """
    Orders.validate_order_list should validate the orders specified
    """
    shipment_refused_by_seller = {'OrderNumber': '1904240959CN8HI',
                                  'OrderState': 'ShipmentRefusedBySeller',
                                  'OrderLineList': [{
                                  'AcceptationState': 'ShipmentRefusedBySeller',
                                  'SellerProductId': 'PRES1',
                                  'ProductCondition': 'AverageState'}]}
    validations = api.orders.prepare_validations([shipment_refused_by_seller])
    response = api.orders.validate_order_list(**validations)
    assert_response_succeeded(response)


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_validate_order_list_with_new_action_not_allowed(api):
    """
    Orders.validate_order_list should return an error response when
    the action chosen is not allowed
    """
    # In this case, the order has already been cancelled.
    # Cancelling it another time is not allowed
    shipment_refused_by_seller = {'OrderNumber': '1904240959CN8HI',
                                  'OrderState': 'ShipmentRefusedBySeller',
                                  'OrderLineList': [{
                                  'AcceptationState': 'ShipmentRefusedBySeller',
                                  'SellerProductId': 'PRES1',
                                  'ProductCondition': 'AverageState'}]}

    validations = api.orders.prepare_validations([shipment_refused_by_seller])
    response = api.orders.validate_order_list(**validations)
    assert response['OperationSuccess'] is True
    assert response['ValidateOrderResults'] is not None
    results = response['ValidateOrderResults']
    assert results['ValidateOrderResult'][0]['Errors']['Error'][0]['ErrorType'] == 'OrderStateIncoherent'


# create_refund_voucher {{{1
# Difficult to test create_refund_voucher with vcr, as the action must be
# run at least once, which will change the state of the order that won't be
# allowed to change the next run.
@pytest.mark.skip
@pytest.mark.vcr()
def test_create_refund_voucher(api):
    request = {
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


@pytest.mark.skip
@pytest.mark.vcr()
def test_create_refund_voucher_with_commercial_gesture(api, refund_voucher_request):
    # CommercialGestureList accepts a single dict
    commercial_gestures = {'Amount': 10, 'MotiveId': 135}
    request = refund_voucher_request
    request['CommercialGestureList'] = [commercial_gestures]
    response = api.orders.create_refund_voucher(**request)
    raise AssertionError


@pytest.mark.skip
@pytest.mark.vcr()
def test_create_refund_voucher_with_commercial_gestures(api, refund_voucher_request):
    # CommercialGestureList accepts a list of dicts
    commercial_gestures = [{'Amount': 10, 'MotiveId': 135},
                           {'Amount': 10, 'MotiveId': 132}]
    request = refund_voucher_request
    request['CommercialGestureList'] = [commercial_gestures]
    response = api.orders.create_refund_voucher(**request)
    raise AssertionError


@pytest.mark.vcr()
def test_create_refund_voucher_with_invalid_data(api):
    response = api.orders.create_refund_voucher()
    assert_response_failed(response)
    assert response['CommercialGestureList'] is None
    assert response['OrderNumber'] is None
    assert response['SellerRefundList'] is None


# manage_parcel {{{1
@pytest.mark.vcr()
def test_manage_parcel_without_argument(api):
    response = api.orders.manage_parcel()
    assert_response_failed(response)
    assert response['ParcelActionResultList'] is None


@pytest.mark.vcr()
def test_manage_parcel_with_nonexistent_order(api):
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


@pytest.mark.vcr()
def test_manage_parcel_with_internal_order(api):
    parcel_actions_list = [
        {
            'ManageParcel': 'AskingForDeliveryCertification',
            'ParcelNumber': 'TN1',
            'Sku': 'PRES1',
         }
    ]
    response = api.orders.manage_parcel(
        parcel_actions_list=parcel_actions_list, scopus_id='1904241640CLE8'
    )
    assert_response_failed(response)
    assert response['ParcelActionResultList'] is None
