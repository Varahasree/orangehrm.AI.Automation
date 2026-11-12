
import os
import pytest
import requests
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


load_dotenv()


@pytest.mark.integration
def test_employee_data_matches_between_ui_and_api(
    driver,
    api_client,
    employee_id
):

    # --------------------------------------------------
    # 1. CONFIGURATION
    # --------------------------------------------------

    base_url = os.getenv("ORANGEHRM_URL")
    api_base_url = os.getenv("ORANGEHRM_API_BASE_URL")
    employee_endpoint = os.getenv("ORANGEHRM_EMPLOYEE_ENDPOINT")
    api_token = os.getenv("ORANGEHRM_API_TOKEN")

    if not all([
        base_url,
        api_base_url,
        employee_endpoint,
        api_token
    ]):
        pytest.fail("OrangeHRM configuration is missing")

    employee_id = str(employee_id).strip()

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    collection_url = (
        f"{api_base_url.rstrip('/')}/"
        f"{employee_endpoint.strip('/')}"
    )

    print("\n===================================")
    print("UI AND API EMPLOYEE INTEGRATION TEST")
    print("===================================")

    print("Website Employee ID:", employee_id)

    # --------------------------------------------------
    # 2. FETCH EMPLOYEES FROM API
    # --------------------------------------------------

    print("\nSearching for employee in API...")

    api_employees = []
    offset = 0
    limit = 50

    while True:

        response = requests.get(
            collection_url,
            headers=headers,
            params={
                "limit": limit,
                "offset": offset
            },
            timeout=20
        )

        assert response.status_code == 200, (
            f"Employee API failed.\n"
            f"Status: {response.status_code}\n"
            f"Response: {response.text}"
        )

        records = response.json().get("data", [])

        if not records:
            break

        api_employees.extend(records)

        if len(records) < limit:
            break

        offset += len(records)

    print("Total API employees:", len(api_employees))

    # --------------------------------------------------
    # 3. MAP EMPLOYEE ID TO INTERNAL EMP NUMBER
    # --------------------------------------------------

    matching_employee = next(
        (
            employee
            for employee in api_employees
            if str(employee.get("employeeId") or "").strip()
            == employee_id
        ),
        None
    )

    assert matching_employee is not None, (
        f"Employee ID {employee_id!r} not found in API"
    )

    emp_number = matching_employee.get("empNumber")

    assert emp_number is not None, (
        f"Internal employee number not found for {employee_id}"
    )

    print("\nEMPLOYEE MAPPING SUCCESSFUL")
    print("---------------------------")
    print("Website Employee ID:", employee_id)
    print("Internal Employee Number:", emp_number)

    # --------------------------------------------------
    # 4. FETCH INDIVIDUAL EMPLOYEE FROM API
    # --------------------------------------------------

    detail_url = f"{collection_url}/{emp_number}"

    response = requests.get(
        detail_url,
        headers=headers,
        timeout=20
    )

    assert response.status_code == 200, (
        f"Employee details API failed.\n"
        f"Status: {response.status_code}\n"
        f"Response: {response.text}"
    )

    api_employee = response.json().get("data", {})

    api_first_name = (
        api_employee.get("firstName") or ""
    ).strip()

    api_last_name = (
        api_employee.get("lastName") or ""
    ).strip()

    api_employee_id = str(
        api_employee.get("employeeId") or ""
    ).strip()

    print("\nAPI EMPLOYEE DETAILS")
    print("--------------------")
    print("First Name:", api_first_name)
    print("Last Name:", api_last_name)
    print("Employee ID:", api_employee_id)

    # --------------------------------------------------
    # 5. OPEN EMPLOYEE DETAILS PAGE
    # --------------------------------------------------

    wait = WebDriverWait(driver, 30)

    employee_ui_url = (
        f"{base_url.rstrip('/')}/web/index.php/pim/"
        f"viewPersonalDetails/empNumber/{emp_number}"
    )

    print("\nOpening employee details page...")
    print("URL:", employee_ui_url)

    driver.get(employee_ui_url)

    wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".oxd-layout")
        )
    )

    # --------------------------------------------------
    # 6. DEBUG ACTUAL EMPLOYEE DETAILS PAGE
    # --------------------------------------------------

    print("\n========== PAGE DEBUG ==========")

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)

    print("\nVISIBLE PAGE TEXT:")

    print(
        driver.find_element(
            By.TAG_NAME, "body"
        ).text[:5000]
    )

    print("\nALL INPUT ELEMENTS:")

    all_inputs = driver.find_elements(
        By.TAG_NAME, "input"
    )

    for index, element in enumerate(all_inputs):

        print(
            f"\nINPUT {index}",
            "\nName:", element.get_attribute("name"),
            "\nType:", element.get_attribute("type"),
            "\nValue:", element.get_attribute("value"),
            "\nPlaceholder:", element.get_attribute("placeholder"),
            "\nVisible:", element.is_displayed(),
            "\nEnabled:", element.is_enabled()
        )

        if element.get_attribute("name") in [
            "firstName",
            "lastName"
        ]:
            print(
                "HTML:",
                element.get_attribute("outerHTML")
            )

    print("\nALL LABELS:")

    for label in driver.find_elements(
            By.TAG_NAME, "label"
    ):

        if label.is_displayed():
            print("LABEL:", repr(label.text))

    print("\n================================")

    # Save screenshot
    from pathlib import Path

    Path("reports/screenshots").mkdir(
        parents=True,
        exist_ok=True
    )

    driver.save_screenshot(
        "reports/screenshots/employee_details_debug.png"
    )

    print(
        "\nDebug screenshot saved:"
        " reports/screenshots/employee_details_debug.png"
    )

    # --------------------------------------------------
    # 7. READ EMPLOYEE DETAILS FROM UI
    # --------------------------------------------------

    # First Name
    first_name_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "firstName")
        )
    )

    ui_first_name = (
            first_name_field.get_attribute("value") or ""
    ).strip()

    # Last Name
    last_name_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "lastName")
        )
    )

    ui_last_name = (
            last_name_field.get_attribute("value") or ""
    ).strip()

    # Employee ID
    # This input does not have a name attribute.
    # Locate it using the Employee Id label.

    employee_id_xpath = (
        "//label[normalize-space()='Employee Id']"
        "/following::input[1]"
    )

    employee_id_field = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, employee_id_xpath)
        )
    )

    ui_employee_id = (
            employee_id_field.get_attribute("value") or ""
    ).strip()

    print("\nUI EMPLOYEE DETAILS")
    print("-------------------")
    print("First Name:", ui_first_name)
    print("Last Name:", ui_last_name)
    print("Employee ID:", ui_employee_id)

    # --------------------------------------------------
    # 8. VALIDATE UI VALUES
    # --------------------------------------------------

    assert ui_first_name, "UI First Name is empty"

    assert ui_last_name, "UI Last Name is empty"

    assert ui_employee_id, "UI Employee ID is empty"

    # --------------------------------------------------
    # 9. COMPARE UI AND API
    # --------------------------------------------------

    assert ui_first_name.casefold() == api_first_name.casefold(), (
        f"First Name mismatch: "
        f"UI={ui_first_name!r}, API={api_first_name!r}"
    )

    assert ui_last_name.casefold() == api_last_name.casefold(), (
        f"Last Name mismatch: "
        f"UI={ui_last_name!r}, API={api_last_name!r}"
    )

    assert ui_employee_id == api_employee_id, (
        f"Employee ID mismatch: "
        f"UI={ui_employee_id!r}, API={api_employee_id!r}"
    )

    # --------------------------------------------------
    # 10. FINAL RESULT
    # --------------------------------------------------

    print("\n===================================")
    print("SUCCESS: UI AND API DATA MATCH!")
    print("===================================")

    print("Website Employee ID:", employee_id)
    print("Internal Employee Number:", emp_number)
    print("First Name:", ui_first_name)
    print("Last Name:", ui_last_name)
    print("Employee ID:", ui_employee_id)
