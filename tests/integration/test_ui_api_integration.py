
import os

import pytest
import requests


@pytest.mark.integration
def test_employee_data_matches_between_ui_and_api():
    api_base_url = os.getenv("ORANGEHRM_API_BASE_URL")
    employee_endpoint = os.getenv("ORANGEHRM_EMPLOYEE_ENDPOINT")
    api_token = os.getenv("ORANGEHRM_API_TOKEN")
    employee_id = os.getenv("TEST_EMPLOYEE_ID")
    expected_first_name = os.getenv("TEST_EMPLOYEE_FIRST_NAME")
    expected_last_name = os.getenv("TEST_EMPLOYEE_LAST_NAME")

    required_settings = {
        "ORANGEHRM_API_BASE_URL": api_base_url,
        "ORANGEHRM_EMPLOYEE_ENDPOINT": employee_endpoint,
        "ORANGEHRM_API_TOKEN": api_token,
        "TEST_EMPLOYEE_ID": employee_id,
        "TEST_EMPLOYEE_FIRST_NAME": expected_first_name,
        "TEST_EMPLOYEE_LAST_NAME": expected_last_name,
    }

    missing = [
        key for key, value in required_settings.items()
        if not value
    ]

    if missing:
        pytest.skip(
            "Configure OrangeHRM integration settings: "
            + ", ".join(missing)
        )

    url = (
        f"{api_base_url.rstrip('/')}/"
        f"{employee_endpoint.lstrip('/')}"
    )

    response = requests.get(
        url,
        params={"id": employee_id},
        headers={"Authorization": f"Bearer {api_token}"},
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    # Adapt these field names to your actual API response.
    employee = data.get("data", data)

    assert str(employee["id"]) == employee_id
    assert employee["firstName"] == expected_first_name
    assert employee["lastName"] == expected_last_name
