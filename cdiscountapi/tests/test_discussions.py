import os
import pytest
from ..cdiscountapi import Connection
from unittest import skip
from . import assert_response_succeeded
import datetime


@pytest.mark.vcr()
def test_get_offer_question_list_by_status():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    # Case where there are no offer questions closed
    response = api.discussions.get_offer_question_list(
        StatusList={'DiscussionStateFilter': 'Closed'}
    )
    assert_response_succeeded(response)
    assert response['OfferQuestionList'] is None


@pytest.mark.vcr()
def test_get_offer_question_list_by_date():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    # Case where there are no offer question between the selected creation
    # dates
    dtime = datetime.datetime(2077, 1, 1, 9, 0)

    offer_question_filters = [
        {
            'BeginCreationDate': dtime,
            'EndCreationDate': dtime + datetime.timedelta(days=10)
        },
        {
            'BeginModificationDate': dtime,
            'EndModificationDate': dtime + datetime.timedelta(days=10)
        },
    ]

    for offer_question_filter in offer_question_filters:
        response = api.discussions.get_offer_question_list(
            **offer_question_filter
        )
        assert_response_succeeded(response)
        assert response['OfferQuestionList'] is None


@skip('Standby')
@pytest.mark.vcr()
def test_get_offer_question_list_by_eans():
    pass


@skip('Standby')
@pytest.mark.vcr()
def test_get_offer_question_list_by_seller_refrences():
    pass
