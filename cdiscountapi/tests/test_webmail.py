import os
import pytest
from ..cdiscountapi import Connection
from unittest import skip
from . import assert_response_succeeded, assert_response_failed


@skip('Waiting for orders')
@pytest.mark.vcr()
def test_generate_mail_discussion_guid():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.webmail.generate_mail_discussion_guid('SCOPUS_ID')


@pytest.mark.vcr()
def test_generate_mail_discussion_guid_with_invalid_scopus_id():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.webmail.generate_discussion_mail_guid('INVALID_SCOPUS_ID')
    assert response['ErrorMessage'] is None
    assert response['MailGuid'] is None


@pytest.mark.vcr()
def test_generate_mail_discussion_guid_without_scopus_id():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
    response = api.webmail.generate_discussion_mail_guid()
    assert_response_failed(response)
    assert response['MailGuid'] is None
    assert response['ErrorMessage'] is not None


@pytest.mark.vcr()
def test_get_discussion_mail_list_with_nonexistent_discussions():
    api = Connection(os.getenv('CDISCOUNT_API_LOGIN'),
                     os.getenv('CDISCOUNT_API_PASSWORD'))
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
