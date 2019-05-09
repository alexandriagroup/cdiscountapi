# Python imports
import datetime

# Third-party imports
import pytest
import zeep

# Project imports
from cdiscountapi.packages import OfferPackage


# OfferPackage
@pytest.mark.vcr()
def test_OfferPackage(valid_offer):
    package = OfferPackage({'OfferCollection': [valid_offer]})
    assert len(package.data) == 1
    offer = package.data[0]
    assert offer.Price == valid_offer['Price']
    assert offer.SellerProductId == valid_offer['SellerProductId']
    assert offer.DiscountList == valid_offer['SellerProductId']


@pytest.mark.vcr()
def test_OfferPackage_with_invalid_key(valid_offer):
    invalid_offer = valid_offer
    invalid_offer['InvalidKey'] = 'Unknown'
    # A TypeError should be raised because shipping_info2 has an invalid key
    pytest.raises(TypeError, OfferPackage, {'OfferCollection': [invalid_offer]})


# ProductPackage
@pytest.mark.skip(reason='Stand by')
def test_validate_product():
    raise AssertionError


@pytest.mark.skip(reason='Stand by')
def test_validate_product_with_invalid_key():
    raise AssertionError
