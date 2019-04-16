import os
import pytest
from ..cdiscountapi import Connection
from . import assert_response_succeeded, CDISCOUNT_WITHOUT_DATA
import datetime


# close_discussion
@pytest.mark.vcr()
def test_close_discussion_not_found():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.discussions.close_discussion_list(
        [-2, -1]
    )
    assert_response_succeeded(response)
    assert response['CloseDiscussionResultList'] == {
        'CloseDiscussionResult': [
            {
                'DiscussionId': -2,
                'OperationStatus': 'DiscussionNotFound'
            },
            {
                'DiscussionId': -1,
                'OperationStatus': 'DiscussionNotFound'
            }
        ]
    }


# offer_question
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


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_offer_question_list_by_eans():
    pass


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_offer_question_list_by_seller_refrences():
    pass


# order_question
@pytest.mark.vcr()
def test_get_order_question_list_by_status():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    # Case where there are no order questions closed
    response = api.discussions.get_order_question_list(
        StatusList={'DiscussionStateFilter': 'Closed'}
    )
    assert_response_succeeded(response)
    assert response['OrderQuestionList'] is None


@pytest.mark.vcr()
def test_get_order_question_list_by_date():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))

    # Case where there are no order question between the selected creation
    # dates
    dtime = datetime.datetime(2077, 1, 1, 9, 0)

    order_question_filters = [
        {
            'BeginCreationDate': dtime,
            'EndCreationDate': dtime + datetime.timedelta(days=10)
        },
        {
            'BeginModificationDate': dtime,
            'EndModificationDate': dtime + datetime.timedelta(days=10)
        },
    ]

    for order_question_filter in order_question_filters:
        response = api.discussions.get_order_question_list(
            **order_question_filter
        )
        assert_response_succeeded(response)
        assert response['OrderQuestionList'] is None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_order_question_list_by_eans():
    pass


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_order_question_list_by_seller_refrences():
    pass
