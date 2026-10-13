
import pytest

from Framework.api.api_client import APIClient


@pytest.mark.api
def test_get_existing_user():
    client = APIClient()

    try:
        response = client.get("/users/1")

        assert response.status_code == 200

        user = response.json()
        assert user["id"] == 1
        assert isinstance(user["name"], str)
        assert user["name"].strip() != ""
        assert isinstance(user["email"], str)
        assert "@" in user["email"]
    finally:
        client.close()


@pytest.mark.api
def test_get_non_existing_user():
    client = APIClient()

    try:
        response = client.get("/users/999999")

        assert response.status_code == 404
    finally:
        client.close()


@pytest.mark.api
def test_get_existing_user(api_client):
    response = api_client.get("/users/1")

    assert response.status_code == 200

    user = response.json()
    assert user["id"] == 1
    assert user["name"].strip() != ""