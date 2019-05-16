import pytest
from . import assert_response_succeeded, assert_response_failed, CDISCOUNT_WITHOUT_DATA


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for orders')
@pytest.mark.vcr()
def test_generate_mail_discussion_guid(api):
    response = api.webmail.generate_discussion_mail_guid('1904291413BT4WY')
    assert_response_succeeded(response)
    assert response['MailGuid'] is not None


@pytest.mark.vcr()
def test_generate_discussion_mail_guid_with_invalid_order_id(api):
    response = api.webmail.generate_discussion_mail_guid('INVALID_ORDER_ID')
    assert response['ErrorMessage'] is None
    assert response['MailGuid'] is None


@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason='Waiting for offers')
@pytest.mark.vcr()
def test_get_discussion_mail_list(api):
    response = api.webmail.get_discussion_mail_list([113163877])
    assert_response_succeeded(response)
    assert response['DiscussionMailList']['DiscussionMail'][0]['DiscussionId'] == 113163877
    assert response['DiscussionMailList']['DiscussionMail'][0]['OperationStatus'] == 'DiscussionClosed'
    assert response['DiscussionMailList']['DiscussionMail'][0]['MailAddress'] is not None


@pytest.mark.vcr()
def test_get_discussion_mail_list_with_nonexistent_discussions(api):
    response = api.webmail.get_discussion_mail_list([1, 2])
    assert_response_succeeded(response)
    assert response['DiscussionMailList'] == {
        'DiscussionMail': [{'DiscussionId': 1,
                            'MailAddress': None,
                            'OperationStatus': 'UnknownError'},
                           {'DiscussionId': 2,
                            'MailAddress': None,
                            'OperationStatus': 'UnknownError'}]
    }
