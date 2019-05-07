# Python imports
import datetime
import os
import re
from copy import deepcopy

# Third-party imports
import pytest

# Project imports
from cdiscountapi.cdiscountapi import Connection
from cdiscountapi.helpers import (
    XmlGenerator,
    check_element,
)
from . import assert_response_succeeded


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
def test_XmlGenerator_constructor():
    """
    XmlGenerator should raise a ValueError if the package_type is not 'Offers.xml' or 'products.xml'
    """
    XmlGenerator('Offers.xml')
    XmlGenerator('Products.xml')
    pytest.raises(ValueError, XmlGenerator, 'other.xml')


@pytest.mark.vcr()
def test_add_offers(valid_offer):
    """
    XmlGenerator.add_offers should append the unique valid offers in the attribute `XmlGenerator.offers`
    """
    xml_generator = XmlGenerator()
    assert len(xml_generator.offers) == 0

    xml_generator.add_offers([valid_offer, valid_offer])

    # The should be only 1 valid offer (we added 2 times the same offer)
    assert len(xml_generator.offers) == 1

    # We create a new valid offer with a different DiscountValue
    valid_offer1 = deepcopy(valid_offer)
    valid_offer1['DiscountList'][0]['DiscountValue'] = 10
    xml_generator.add_offers([valid_offer1])

    # The should be 2 valid offers
    assert len(xml_generator.offers) == 2


@pytest.mark.vcr()
def test_add_offers_with_invalid_offer(valid_offer):
    """
    XmlGenerator.add_offers should raise a TypeError when the offer is invalid
    """
    invalid_offer = {'invalid_offer': True}
    xml_generator = XmlGenerator()
    pytest.raises(TypeError, xml_generator.add_offers, [valid_offer, invalid_offer])


@pytest.mark.vcr()
def test_render_offers(valid_offer):
    """
    XmlGenerator.render_offers should return the content of Offers.xml
    """
    valid_offer1 = deepcopy(valid_offer)
    valid_offer1['Price'] = 20
    valid_offer1['SellerProductId'] = 'MY_SKU2'
    xml_generator = XmlGenerator()
    xml_generator.add_offers([valid_offer, valid_offer1])
    content = xml_generator.render_offers()

    with open('cdiscountapi/tests/samples/Offers.xml') as f:
        expected_content = f.read()
    assert content.strip() == expected_content.strip()

# auto_refresh_token
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
