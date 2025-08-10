import pytest

from src.api.client import APIClient


@pytest.mark.api
def test_get_user(test_data):
    api_url = "https://reqres.in/api"
    api_client = APIClient(base_url=api_url)
    path = test_data["api"]["path"]
    user_id = test_data["api"]["user_id"]

    try:
        response = api_client.get_user(path, user_id)

        # Basic response checks
        assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        json_data = response.json()
        assert json_data["data"]["id"] == user_id, "User ID does not match"
        assert "email" in json_data["data"], "Email field missing"
    except Exception as ex:
        pytest.fail(f"Unexpected exception: {ex}")
