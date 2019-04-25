import os
import pytest
from . import assert_response_succeeded, CDISCOUNT_WITHOUT_DATA
import datetime


# close_discussion
@pytest.mark.vcr()
def test_close_discussion(api):
    response = api.discussions.close_discussion_list([113157784])
    assert_response_succeeded(response)
    assert 'CloseDiscussionResultList' in response


@pytest.mark.vcr()
def test_close_discussion_not_found(api):
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
def test_get_offer_question_list(api):
    response = api.discussions.get_offer_question_list()
    assert_response_succeeded(response)
    assert 'OfferQuestionList' in response


@pytest.mark.vcr()
def test_get_offer_question_list_by_status(api):
    response = api.discussions.get_offer_question_list(
        StatusList={'DiscussionStateFilter': 'Closed'}
    )
    assert_response_succeeded(response)
    # If there are closed questions, OfferQuestionList should not be None
    assert response['OfferQuestionList'] is not None


@pytest.mark.vcr()
def test_get_offer_question_list_by_date(api):
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


# We created some data for the tests:
# ProductEANList: '2009863600561'
# ProductSellerReference: 'PRES1'

@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_offer_question_list_by_eans(api):
    response = api.discussions.get_offer_question_list(ProductEANList=['2009863600561'])
    assert_response_succeeded(response)
    assert response['OfferQuestionList'] is not None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
@pytest.mark.vcr()
def test_get_offer_question_list_by_seller_refrences(api):
    response = api.discussions.get_offer_question_list(ProductSellerReferenceList=['PRES1'])
    assert_response_succeeded(response)
    assert response['OfferQuestionList'] is not None


# order_question
@pytest.mark.vcr()
def test_get_order_question_list_by_status(api):
    # Case where there are no order questions closed
    response = api.discussions.get_order_question_list(
        StatusList={'DiscussionStateFilter': 'Closed'}
    )
    assert_response_succeeded(response)
    assert response['OrderQuestionList'] is None


@pytest.mark.vcr()
def test_get_order_question_list_by_date(api):
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


@pytest.mark.vcr()
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
def test_get_order_question_list_by_eans(api):
    pass


@pytest.mark.vcr()
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Stand by')
def test_get_order_question_list_by_seller_refrences(api):
    pass


# get_order_claim_list
@pytest.mark.vcr()
def test_get_order_claim_list(api):
    response = api.discussions.get_order_claim_list()
    assert_response_succeeded(response)
    assert 'OrderClaimList' in response
