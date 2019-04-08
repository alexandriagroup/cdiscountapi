import os
import pytest
from ..cdiscountapi import Connection
from . import assert_response_succeeded
from unittest import skip


# TODO Regenerate the cassette with the correct response
@skip('Finish TODO')
@pytest.mark.vcr()
def test_get_offer_list_without_offers():
    """
    get_offer_list should return the correct information when there's no offer
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.offers.get_offer_list()
    assert_response_succeeded(response)
    # OfferList should be None
    assert response['OfferList'] is None
