import pytest

from src.api.client import APIClient


@pytest.mark.api
def test_get_user(test_data):
    base_url = test_data["api"]["base_url"]
    user_id = test_data["api"]["user_id"]
    api_client = APIClient(base_url=base_url)

    path = f"/users/{user_id}"
    response = api_client.get(path)

    # Basic response checks
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    json_data = response.json()
    assert json_data["data"]["id"] == user_id, "User ID does not match"
    assert "email" in json_data["data"], "Email field missing"
