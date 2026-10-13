
import pytest

from Framework.api.api_client import APIClient


@pytest.mark.api
def test_api_returns_successful_response():
    client = APIClient()

    try:
        response = client.get("/users/1")

        assert response.status_code == 200
        assert response.headers.get(
            "Content-Type", ""
        ).startswith("application/json")

        data = response.json()
        assert isinstance(data, dict)
        assert "id" in data
        assert "name" in data
    finally:
        client.close()