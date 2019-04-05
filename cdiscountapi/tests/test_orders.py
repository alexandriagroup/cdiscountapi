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
