# Python imports
import os
import re
from copy import deepcopy

# Third-party imports
import pytest

# Project imports
from cdiscountapi import Connection
from cdiscountapi.helpers import XmlGenerator, check_element
from cdiscountapi.exceptions import ValidationError
from . import (
    SAMPLES_DIR,
    assert_response_succeeded,
    assert_xml_files_equal,
    discount_component
)


@pytest.mark.vcr()
def test_check_element_with_valid_element(api):
    """
    check_element should return None when the element is valid for the XSD type
    """
    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert "CarrierName" in valid_elements
    assert check_element("CarrierName", dynamic_type) is None


@pytest.mark.vcr()
def test_check_element_with_invalid_element(api):
    """
    check_element should raise a TypeError when the element is invalid for the
    XSD type
    """
    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert "INVALID_ELEMENT" not in valid_elements
    pytest.raises(TypeError, check_element, "INVALID_ELEMENT", dynamic_type)


# XmlGenerator
@pytest.mark.vcr()
def test_XmlGenerator_constructor(valid_offer_for_package):
    """
    XmlGenerator should raise a ValueError if `data` isn't a dictionary with the key
    'OfferCollection' for Offers.xml and 'Products' for Products.xml
    """
    XmlGenerator({"OfferCollection": [{"Offer": valid_offer_for_package}]})
    XmlGenerator({"Products": []})
    pytest.raises(
        ValueError, XmlGenerator, {"InvalidKey": [{"Offer": valid_offer_for_package}]}
    )


@pytest.mark.vcr()
def test_add_offers(valid_offer_for_package):
    """
    XmlGenerator.add should append the unique valid offers in the
    attribute `XmlGenerator.data`
    """
    xml_generator = XmlGenerator({
        "OfferCollection": [{"Offer": valid_offer_for_package}],
        "Name": "A good package"
    })
    assert len(xml_generator.data) == 1

    xml_generator.add([{"Offer": valid_offer_for_package}])

    # The should be only 1 valid offer (we added 2 times the same offer)
    assert len(xml_generator.data) == 1

    # We create a new valid offer with a DiscountList
    valid_offer_for_package1 = deepcopy(valid_offer_for_package)
    valid_offer_for_package1["DiscountList"] = {
        "DiscountComponent": [discount_component()]
    }
    xml_generator.add([{"Offer": valid_offer_for_package1}])

    # There should be 2 valid offers
    assert len(xml_generator.data) == 2


@pytest.mark.vcr()
def test_add_offers_with_invalid_offer(valid_offer_for_package):
    """
    XmlGenerator.add should raise a TypeError when the offer is invalid
    """
    xml_generator = XmlGenerator({"OfferCollection": [{"Offer": valid_offer_for_package}]})
    invalid_offer_for_package = {"invalid_offer": True}
    pytest.raises(
        ValidationError,
        xml_generator.add,
        [{"Offer": valid_offer_for_package}, {"Offer": invalid_offer_for_package}],
    )


@pytest.mark.vcr()
def test_generate_offers(valid_offer_for_package):
    """
    XmlGenerator.generate should return the content of Offers.xml
    """
    # We add a second offer in the package
    valid_offer_for_package1 = deepcopy(valid_offer_for_package)
    valid_offer_for_package1["Price"] = 20
    valid_offer_for_package1["SellerProductId"] = "MY_SKU2"
    xml_generator = XmlGenerator({
        "OfferCollection": [{"Offer": valid_offer_for_package}],
        "Name": "A good package"
    })
    xml_generator.add([{"Offer": valid_offer_for_package}, {"Offer": valid_offer_for_package1}])
    content = xml_generator.generate()

    with open(SAMPLES_DIR.joinpath("offers", "Offers.xml")) as f:
        expected_content = f.read()

    assert_xml_files_equal(content, expected_content, "Offer")


@pytest.mark.vcr()
def test_generate_offers_with_discount(valid_offer_for_package):
    """
    XmlGenerator.generate should return the content of Offers.xml
    """
    # We add a second offer in the package
    valid_offer_for_package1 = deepcopy(valid_offer_for_package)
    valid_offer_for_package1["Price"] = 20
    valid_offer_for_package1["SellerProductId"] = "MY_SKU2"
    # Only the first offer has a DiscountList
    valid_offer_for_package["DiscountList"] = {
        "DiscountComponent": [discount_component()]
    }

    xml_generator = XmlGenerator({
        "OfferCollection": [{"Offer": valid_offer_for_package}],
        "Name": "A good package"
    })
    xml_generator.add([{"Offer": valid_offer_for_package}, {"Offer": valid_offer_for_package1}])
    content = xml_generator.generate()

    with open(SAMPLES_DIR.joinpath("offers", "Offers_with_discount.xml")) as f:
        expected_content = f.read()

    assert_xml_files_equal(content, expected_content, "Offer")


@pytest.mark.vcr()
def test_generate_offers_with_offer_publication_list(valid_offer_for_package):
    """
    XmlGenerator.generate should return the content of Offers.xml
    """
    # We add a second offer in the package
    valid_offer_for_package1 = deepcopy(valid_offer_for_package)
    valid_offer_for_package1["Price"] = 20
    valid_offer_for_package1["SellerProductId"] = "MY_SKU2"
    xml_generator = XmlGenerator({
        "OfferCollection": [{"Offer": valid_offer_for_package}],
        "Name": "A good package"
    })
    xml_generator.add([{"Offer": valid_offer_for_package}, {"Offer": valid_offer_for_package1}])
    content = xml_generator.generate()

    with open(
        SAMPLES_DIR.joinpath("offers", "Offers_with_offer_publication_list.xml")
    ) as f:
        expected_content = f.read()

    assert_xml_files_equal(content, expected_content, "Offer")


# ProductPackage
@pytest.mark.vcr()
def test_add_products(valid_product_for_package):
    xml_generator = XmlGenerator({"Products": [{"Product": valid_product_for_package}]})
    assert len(xml_generator.data) == 1

    xml_generator.add([{"Product": valid_product_for_package}])

    # The should be only 1 valid offer (we added 2 times the same offer)
    assert len(xml_generator.data) == 1

    # We create a new valid offer with a different DiscountValue
    valid_product1 = deepcopy(valid_product_for_package)
    valid_product1["SellerProductColorName"] = "Bleu Canard"
    xml_generator.add([{"Product": valid_product1}])

    # There should be 2 valid offers
    assert len(xml_generator.data) == 2


@pytest.mark.vcr()
def test_add_products_with_invalid_product(valid_product_for_package):
    xml_generator = XmlGenerator({"Products": [{"Product": valid_product_for_package}]})
    invalid_product = {"invalid_product": True}
    pytest.raises(
        ValidationError, xml_generator.add, [{"Product": valid_product_for_package},
                                             {"Product": invalid_product}]
    )


@pytest.mark.vcr()
def test_generate_products(valid_product_for_package):
    """
    XmlGenerator.generate should return the content of Products.xml
    """
    # We add a second product in the package
    valid_product_for_package1 = deepcopy(valid_product_for_package)
    valid_product_for_package1["EanList"] = {"ProductEan": [{"Ean": "3606918243774"}]}
    valid_product_for_package1["SellerProductId"] = "120905784"
    valid_product_for_package1["Size"] = "36/34"

    xml_generator = XmlGenerator(
        {"Products": [{"Product": valid_product_for_package}, {"Product": valid_product_for_package1}]}
    )
    xml_generator.add([{"Product": valid_product_for_package}])
    content = xml_generator.generate()

    with open(SAMPLES_DIR.joinpath("products", "Products.xml")) as f:
        expected_content = f.read()

    assert_xml_files_equal(content, expected_content, "Product")


# auto_refresh_token
@pytest.mark.vcr()
def test_auto_refresh_token():
    # We get rid of the fixture 'api' that has a cache because we want to do a
    # new request to the server
    api = Connection(
        os.getenv("CDISCOUNT_API_LOGIN"),
        os.getenv("CDISCOUNT_API_PASSWORD"),
        header_message={
            "Context": {"SiteID": 100, "CatalogID": 1},
            "Localization": {"Country": "Fr"},
            "Security": {"UserName": ""},
            "Version": "1.0",
        },
    )

    # We purposely set an invalid token so that a zeep.exceptions.Fault is raised
    api.header["Security"]["TokenId"] = "invalid_token"
    api.token = "invalid_token"
    # Then we run any operation
    response = api.seller.get_seller_info()
    assert_response_succeeded(response)

    # The token should be valid now
    assert api.token == api.header["Security"]["TokenId"]
    assert re.match(r"[a-z0-9]{32}", api.token) is not None
