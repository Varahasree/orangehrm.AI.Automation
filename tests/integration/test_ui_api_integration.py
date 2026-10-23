
import os

import pytest
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.integration
def test_employee_data_matches_between_ui_and_api():
    # Read configuration
    api_base_url = os.getenv("ORANGEHRM_API_BASE_URL")
    employee_endpoint = os.getenv("ORANGEHRM_EMPLOYEE_ENDPOINT")
    api_token = os.getenv("ORANGEHRM_API_TOKEN")
    employee_id = os.getenv("TEST_EMPLOYEE_ID")
    username = os.getenv("ORANGEHRM_USERNAME")
    password = os.getenv("ORANGEHRM_PASSWORD")

    required_settings = {
        "ORANGEHRM_API_BASE_URL": api_base_url,
        "ORANGEHRM_EMPLOYEE_ENDPOINT": employee_endpoint,
        "ORANGEHRM_API_TOKEN": api_token,
        "TEST_EMPLOYEE_ID": employee_id,
        "ORANGEHRM_USERNAME": username,
        "ORANGEHRM_PASSWORD": password,
    }

    missing = [
        key for key, value in required_settings.items()
        if not value
    ]

    if missing:
        pytest.skip(
            "Configure integration settings: " + ", ".join(missing)
        )

    # 1. Get employee details from API
    api_url = (
        f"{api_base_url.rstrip('/')}/"
        f"{employee_endpoint.strip('/')}/"
        f"{employee_id}"
    )

    response = requests.get(
        api_url,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
        },
        timeout=15,
    )

    assert response.status_code == 200, (
        f"API request failed: {response.status_code} - "
        f"{response.text}"
    )

    api_employee = response.json()["data"]

    assert str(api_employee["empNumber"]) == employee_id

    # 2. Open the actual OrangeHRM UI in Chrome
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)

    try:
        login_url = (
            f"{api_base_url.rstrip('/')}/auth/login"
        )
        driver.get(login_url)

        # Log in
        wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        ).send_keys(username)

        driver.find_element(
            By.NAME, "password"
        ).send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        # Wait until login has completed
        wait.until(
            EC.url_contains("/dashboard/index")
        )

        # 3. Open the selected employee's personal details
        employee_ui_url = (
            f"{api_base_url.rstrip('/')}/"
            f"pim/viewPersonalDetails/empNumber/"
            f"{employee_id}"
        )

        driver.get(employee_ui_url)

        # Wait for the employee details page to load
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//form")
            )
        )

        first_name_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='firstName']")
            )
        )

        wait.until(
            lambda driver: first_name_field.get_attribute("value").strip() != ""
        )

        ui_first_name = first_name_field.get_attribute("value").strip()

        last_name_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@name='lastName']")
            )
        )

        wait.until(
            lambda driver: last_name_field.get_attribute("value").strip() != ""
        )

        ui_last_name = last_name_field.get_attribute("value").strip()

        employee_id_field = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//label[normalize-space()='Employee Id']"
                    "/ancestor::div[contains(@class,'oxd-input-group')]"
                    "//input",
                )
            )
        )

        # 4. Read the values actually displayed in the UI
        ui_first_name = first_name_field.get_attribute("value")
        ui_last_name = last_name_field.get_attribute("value")
        ui_employee_id = employee_id_field.get_attribute("value")

        # 5. Compare UI values with API values
        assert ui_first_name == api_employee["firstName"], (
            f"First name mismatch: UI={ui_first_name!r}, "
            f"API={api_employee['firstName']!r}"
        )

        assert ui_last_name == api_employee["lastName"], (
            f"Last name mismatch: UI={ui_last_name!r}, "
            f"API={api_employee['lastName']!r}"
        )

        assert ui_employee_id == api_employee["employeeId"], (
            f"Employee ID mismatch: UI={ui_employee_id!r}, "
            f"API={api_employee['employeeId']!r}"
        )

        print("\nUI and API employee data match!")
        print(f"Employee number: {employee_id}")
        print(f"First name: {ui_first_name}")
        print(f"Last name: {ui_last_name}")
        print(f"Employee ID: {ui_employee_id}")

    finally:
        driver.quit()
