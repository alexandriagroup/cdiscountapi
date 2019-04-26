# Python imports
import os
import re
import json
import datetime
from tempfile import gettempdir
from shutil import rmtree

# Third-party imports
import pytest

# Project imports
from cdiscountapi.cdiscountapi import Connection
from cdiscountapi.helpers import (
    check_element, generate_offer_package, generate_product_package,
    XmlGenerator
)
from . import assert_response_succeeded


@pytest.mark.vcr()
def test_generate_product_package():
    path = gettempdir()
    # Check uploading_package doesn't exists yet.
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False

    # Get product_dict from json file.
    filename = 'cdiscountapi/tests/samples/products/products_to_submit.json'
    with open(filename, 'r') as f:
        product_dict = json.load(f)

    # Generate packages.
    generate_product_package(path, product_dict)

    # Check uploading_package exists now.
    assert 'uploading_package' in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is True

    # Get expected Products.xml.
    filename = 'cdiscountapi/tests/samples/products/Products.xml'
    with open(filename, 'r') as f:
        expected = f.read()

    # Get created Products.xml.
    filename = f'{path}/uploading_package/Content/Products.xml'
    with open(filename, 'r') as f:
        created = f.read()

    # Check Products.xml is ok.
    assert created == expected

    # Remove temporary files.
    rmtree(f'{path}/uploading_package')
    os.remove(f'{path}/uploading_package.zip')
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False


@pytest.mark.vcr()
def test_generate_offer_package():
    path = gettempdir()
    # Check uploading_package doesn't exists yet.
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False

    # Get offer_dict from json file.
    filename = 'cdiscountapi/tests/samples/offers/offers_to_submit.json'
    with open(filename, 'r') as f:
        offer_dict = json.load(f)

    # Generate packages.
    generate_offer_package(path, offer_dict)

    # Check uploading_package exists now.
    assert 'uploading_package' in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is True

    # Get expected Offers.xml.
    filename = 'cdiscountapi/tests/samples/offers/Offers.xml'
    with open(filename, 'r') as f:
        expected = f.read()

    # Get created Offers.xml.
    filename = f'{path}/uploading_package/Content/Offers.xml'
    with open(filename, 'r') as f:
        created = f.read()

    # Check Offers.xml is ok.
    assert created == expected

    # Remove temporary files.
    rmtree(f'{path}/uploading_package')
    os.remove(f'{path}/uploading_package.zip')
    assert 'uploading_package' not in os.listdir(path)
    assert os.path.isfile(f'{path}/uploading_package.zip') is False


def test_generate_package_url():
    pass


@pytest.mark.vcr()
def test_check_element_with_valid_element(api):
    """
    check_element should return None when the element is valid for the XSD type
    """
    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert 'CarrierName' in valid_elements
    assert check_element('CarrierName', dynamic_type) is None


@pytest.mark.vcr()
def test_check_element_with_invalid_element(api):
    """
    check_element should raise a TypeError when the element is invalid for the
    XSD type
    """
    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert 'INVALID_ELEMENT' not in valid_elements
    pytest.raises(TypeError, check_element, 'INVALID_ELEMENT', dynamic_type)


# XmlGenerator
@pytest.fixture
def valid_offer():
    discount_component = {
        'DiscountValue': 5, 'Type': 1,
        'StartDate': datetime.datetime(2019, 4, 15),
        'EndDate': datetime.datetime(2019, 5, 15)
    }
    shipping_info1 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': 'Standard'
    }
    shipping_info2 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': 'Tracked'
    }
    offer = {
        'DiscountList': [discount_component],
        'ShippingInformationList': [shipping_info1, shipping_info2]
    }
    return offer


@pytest.mark.vcr()
def test_validate_offer(valid_offer):
    generator = XmlGenerator()
    generator.validate_offer(**valid_offer)


@pytest.mark.vcr()
def test_validate_offer_with_invalid_key():
    generator = XmlGenerator()
    discount_component = {
        'DiscountValue': 5, 'Type': 1,
        'StartDate': datetime.datetime(2019, 4, 15),
        'EndDate': datetime.datetime(2019, 5, 15)
    }
    shipping_info1 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'DeliveryMode': 'Standard'
    }
    shipping_info2 = {
        'ShippingCharges': 2, 'AdditionalShippingCharges': 4,
        'InvalidKey': 'Unknown'
    }
    offer = {
        'DiscountList': [discount_component],
        'ShippingInformationList': [shipping_info1, shipping_info2]
    }

    # A TypeError should be raised because shipping_info2 has an invalid key
    pytest.raises(TypeError, generator.validate_offer, offer)


@pytest.mark.skip(reason='Stand by')
@pytest.mark.vcr()
def test_add_offers():
    raise AssertionError


@pytest.mark.vcr()
def test_auto_refresh_token():
    # We get rid of the fixture 'api' that has a cache because we want to do a
    # new request to the server
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'),
                     header_message={
                         'Context': {
                             'SiteID': 100,
                             'CatalogID': 1
                         },
                         'Localization': {
                             'Country': 'Fr',
                         },
                         'Security': {
                             'UserName': '',
                         },
                         'Version': '1.0',
                     })

    # We purposely set an invalid token so that a zeep.exceptions.Fault is raised
    api.header['Security']['TokenId'] = 'invalid_token'
    api.token = 'invalid_token'
    # Then we run any operation
    response = api.seller.get_seller_info()
    assert_response_succeeded(response)

    # The token should be valid now
    assert api.token == api.header['Security']['TokenId']
    assert re.match(r'[a-z0-9]{32}', api.token) is not None
