# Third-party imports
import pytest

# Project imports
from cdiscountapi.packages import OfferPackage, ProductPackage
from cdiscountapi.exceptions import ValidationError


# OfferPackage
@pytest.mark.vcr()
def test_OfferPackage_with_PackageType_Full(valid_offer_for_package):
    # The required keys must be ProductEan and SellerProductId
    package = OfferPackage(
        {"OfferCollection": [{"Offer": valid_offer_for_package}], "PackageType": "Full"}
    )
    assert len(package.data) == 1
    offer_for_package = package.data[0]
    assert offer_for_package == valid_offer_for_package


@pytest.mark.vcr()
def test_OfferPackage_with_PackageType_StockAndPrice(valid_offer_for_package):
    # The required keys must be ProductEan and SellerProductId
    offer = {
        "ProductEan": "978-1593274351", "SellerProductId": 'MY_SKU1', "Price": 10,
    }
    package = OfferPackage(
        {"OfferCollection": [{"Offer": offer}], "PackageType": "StockAndPrice"}
    )
    assert len(package.data) == 1
    offer_for_package = package.data[0]
    assert offer_for_package == offer


@pytest.mark.vcr()
def test_OfferPackage_with_invalid_key(valid_offer_for_package):
    invalid_offer_for_package = valid_offer_for_package
    invalid_offer_for_package["InvalidKey"] = "Unknown"
    # A ValidationError should be raised because InvalidKey is neither required
    # or optional
    pytest.raises(
        ValidationError, OfferPackage, {
            "OfferCollection": [{"Offer": invalid_offer_for_package}]
        }
    )


@pytest.mark.parametrize("key", ["ProductEan", "SellerProductId"])
@pytest.mark.vcr()
def test_OfferPackage_with_missing_key(valid_offer_for_package, key):
    invalid_offer_for_package = valid_offer_for_package
    del invalid_offer_for_package[key]
    # A ValidationError should be raised because ProductEan is required
    pytest.raises(
        ValidationError, OfferPackage, {
            "OfferCollection": [{"Offer": invalid_offer_for_package}]
        }
    )


# ProductPackage
@pytest.mark.vcr()
def test_ProductPackage(valid_product_for_package):
    package = ProductPackage({"Products": [{"Product": valid_product_for_package}]})
    assert len(package.data) == 1
    product_for_package = package.data[0]
    assert product_for_package == valid_product_for_package


@pytest.mark.vcr()
def test_ProductPackage_with_invalid_key(valid_product_for_package):
    invalid_product_for_package = valid_product_for_package
    invalid_product_for_package["InvalidKey"] = "Unknown"
    # A ValidationError should be raised because InvalidKey is neither required
    # or optional
    pytest.raises(
        ValidationError, ProductPackage, {"Products": [{"Product": invalid_product_for_package}]}
    )
