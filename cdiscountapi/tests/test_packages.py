# Third-party imports
import pytest

# Project imports
from cdiscountapi.packages import OfferPackage, ProductPackage
from cdiscountapi.exceptions import ValidationError


# OfferPackage
@pytest.mark.vcr()
def test_OfferPackage(valid_offer_for_package):
    package = OfferPackage({'OfferCollection': [valid_offer_for_package]})
    assert len(package.data) == 1
    offer_for_package = package.data[0]
    assert offer_for_package == valid_offer_for_package


@pytest.mark.vcr()
def test_OfferPackage_with_invalid_key(valid_offer_for_package):
    invalid_offer_for_package = valid_offer_for_package
    invalid_offer_for_package['InvalidKey'] = 'Unknown'
    # A ValidationError should be raised because InvalidKey is neither required
    # or optional
    pytest.raises(ValidationError, OfferPackage, {'OfferCollection':
                                                  [invalid_offer_for_package]})


# ProductPackage
@pytest.mark.skip(reason='Stand by')
def test_validate_product():
    raise AssertionError


@pytest.mark.skip(reason='Stand by')
def test_validate_product_with_invalid_key():
    raise AssertionError
