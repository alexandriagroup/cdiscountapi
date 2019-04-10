import os
import pytest
from ..cdiscountapi import Connection, check_element


@pytest.mark.vcr()
def test_check_element_with_valid_element():
    """
    check_element should return None when the element is valid for the XSD type
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert 'CarrierName' in valid_elements
    assert check_element('CarrierName', dynamic_type) is None


@pytest.mark.vcr()
def test_check_element_with_invalid_element():
    """
    check_element should raise a ValueError when the element is invalid for the
    XSD type
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    dynamic_type = api.factory.ValidateOrder
    valid_elements = [x[0] for x in dynamic_type.elements]
    assert 'INVALID_ELEMENT' not in valid_elements
    pytest.raises(ValueError, check_element, 'INVALID_ELEMENT', dynamic_type)
