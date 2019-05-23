import pytest
from . import assert_response_succeeded, assert_response_failed, CDISCOUNT_WITHOUT_DATA


# TODO Find out how to get a not empty ParcelShopList
@pytest.mark.vcr()
def test_get_parcel_shop_list(api):
    response = api.relays.get_parcel_shop_list()
    assert_response_succeeded(response)
    assert response["ParcelShopList"] is None


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason="Standby")
@pytest.mark.vcr()
def test_submit_relays_file(api):
    response = api.relays.submit_relays_file(RelaysFileURI="")


# TODO Finish this test
@pytest.mark.skipif(CDISCOUNT_WITHOUT_DATA, reason="Standby")
@pytest.mark.vcr()
def test_get_relays_file_submission_result(api):
    response = api.relays.get_relays_file_submission_result(RelaysFileId=1)


@pytest.mark.vcr()
def test_get_relays_file_submission_result_without_relays_file(api):
    """
    With no relays file submitted, Relays.get_relays_file_submission_result
    should return an invalid response when any RelaysFileId is specified
    """
    response = api.relays.get_relays_file_submission_result(
        relays_file_ids=[15645, 52486]
    )
    assert_response_failed(response)
    assert response["RelaysFileIntegrationStatus"] is None
    assert response["RelaysLogList"] == {"RelayIntegrationLog": []}
