import json
import os
from shutil import rmtree
from tempfile import gettempdir
import pytest
from ..cdiscountapi import Connection


@pytest.mark.vcr()
def test_get_offer_list_without_offers():
    """
    get_offer_list should return the correct information when there's no offer
    """
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.offers.get_offer_list()
    assert response['ErrorList'] is None
    assert response['ErrorMessage'] is None
    # OfferList should be None and OperationSuccess should be False
    assert response['OperationSuccess'] is False
    assert response['OfferList'] is None
