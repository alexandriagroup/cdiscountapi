def assert_response_succeeded(response):
    assert response['ErrorList'] is None,\
        'ErrorList should be None but is {}'.format(response['ErrorList'])
    assert response['ErrorMessage'] is None,\
        'ErrorMessage should be None but is {}'.format(response['ErrorMessage'])
    assert response['OperationSuccess'] is True,\
        'OperationSuccess should be True but is {}'.format(response['OperationSuccess'])
