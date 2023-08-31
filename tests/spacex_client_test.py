from http import HTTPStatus

import pytest
import json

from src.core.spacex_api.spacex_api_client import SpaceXAPIClient


@pytest.fixture()
def fake_launches_info():
    """Fixture that returns a static launches data."""
    with open("tests/resources/launches.json") as f:
        return json.load(f)


def test_get_url_based_on_endpoints():
    v4_url = SpaceXAPIClient().get_url_for_endpoint("rockets")
    v5_url = SpaceXAPIClient().get_url_for_endpoint("launches")

    assert v4_url == "https://api.spacexdata.com/v4/rockets"
    assert v5_url == "https://api.spacexdata.com/v5/launches"


def test_retrieval_spacex_data_by_endpoint(mocker, fake_launches_info):
    """Test that launches are retrieved using mocks."""
    fake_resp = mocker.Mock()
    fake_resp.json.return_value = fake_launches_info
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)

    launches_info = SpaceXAPIClient().fetch_data_by_endpoint("launches")
    assert launches_info == fake_launches_info
    assert len(launches_info) == 2


def test_retrieval_spacex_data_by_endpoint_and_id(mocker, fake_launches_info):
    """Test that launches are retrieved using mocks by id."""
    fake_resp = mocker.Mock()
    fake_resp.json.return_value = fake_launches_info[0]
    launch_id = '5eb87cd9ffd86e000604b32a'
    fake_resp.status_code = HTTPStatus.OK
    mocker.patch("requests.get", return_value=fake_resp)

    launches_info = SpaceXAPIClient().fetch_data_by_endpoint_and_id("launches", launch_id)
    assert launches_info.get("id") == launch_id
