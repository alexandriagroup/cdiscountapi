import os


CDISCOUNT_WITHOUT_DATA = True if os.getenv('CDISCOUNT_WITHOUT_DATA') == '1' else False


def assert_response_succeeded(response):
    assert response['ErrorList'] is None,\
        'ErrorList should be None but is {}'.format(response['ErrorList'])
    assert response['ErrorMessage'] is None,\
        'ErrorMessage should be None but is {}'.format(response['ErrorMessage'])
    assert response['OperationSuccess'] is True,\
        'OperationSuccess should be True but is {}'.format(response['OperationSuccess'])


def assert_response_failed(response):
    assert response['ErrorMessage'] is not None,\
        'ErrorMessage should not be None but is {}'.format(response['ErrorMessage'])
    assert response['OperationSuccess'] is False,\
        'OperationSuccess should be False but is {}'.format(response['OperationSuccess'])
