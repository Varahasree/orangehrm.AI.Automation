
import pytest
import json
import os
import random

from pathlib import Path
from datetime import datetime, timezone

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from Framework.driver.driver_factory import DriverFactory
from Framework.api.api_client import APIClient
from Framework.ai.failure_analyzer import FailureAnalyzer
from dotenv import load_dotenv

load_dotenv()

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on"
    )


# --------------------------------------------------
# BROWSER FIXTURE
# --------------------------------------------------

@pytest.fixture
def driver(request):

    browser = request.config.getoption("--browser")

    browser_driver = DriverFactory.create_driver(browser)

    yield browser_driver

    browser_driver.quit()


# --------------------------------------------------
# ORANGEHRM LOGIN
# --------------------------------------------------

def login_to_orangehrm(driver):

    base_url = os.getenv("ORANGEHRM_URL")
    username = os.getenv("ORANGEHRM_USERNAME")
    password = os.getenv("ORANGEHRM_PASSWORD")

    if not all([base_url, username, password]):
        pytest.fail(
            "ORANGEHRM_URL, ORANGEHRM_USERNAME "
            "or ORANGEHRM_PASSWORD is missing"
        )

    wait = WebDriverWait(driver, 25)

    login_url = (
        f"{base_url.rstrip('/')}/web/index.php/auth/login"
    )

    driver.get(login_url)

    username_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "username")
        )
    )

    password_field = wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "password")
        )
    )

    username_field.clear()
    username_field.send_keys(username)

    password_field.clear()
    password_field.send_keys(password)

    driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    ).click()

    wait.until(
        EC.url_contains("/dashboard/index")
    )

    print("\nOrangeHRM login successful")


# --------------------------------------------------
# FETCH EMPLOYEE IDS FROM ORANGEHRM WEBSITE
# --------------------------------------------------

def fetch_employee_ids_from_ui(driver):

    base_url = os.getenv("ORANGEHRM_URL")

    wait = WebDriverWait(driver, 25)

    employee_list_url = (
        f"{base_url.rstrip('/')}/web/index.php/pim/viewEmployeeList"
    )

    driver.get(employee_list_url)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".oxd-table")
        )
    )

    employee_ids = []
    visited_pages = set()

    print("\nReading employee IDs from OrangeHRM website...")

    while True:

        # Wait for table rows to become visible
        try:
            wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".oxd-table-body")
                )
            )
        except TimeoutException:
            pytest.fail(
                "Employee table did not load in OrangeHRM"
            )

        rows = driver.find_elements(
            By.CSS_SELECTOR,
            ".oxd-table-body .oxd-table-row"
        )

        page_ids = []

        for row in rows:

            cells = row.find_elements(
                By.CSS_SELECTOR,
                ".oxd-table-cell"
            )

            # OrangeHRM employee table:
            # Column 0 = Checkbox
            # Column 1 = Employee ID

            if len(cells) >= 2:

                employee_id = cells[1].text.strip()

                if employee_id:
                    page_ids.append(employee_id)

        # Prevent infinite pagination loops
        page_signature = tuple(page_ids)

        if page_signature in visited_pages:
            break

        visited_pages.add(page_signature)

        employee_ids.extend(page_ids)

        print(
            f"Employee IDs found on current page: "
            f"{len(page_ids)}"
        )

        # Find next-page button
        next_buttons = driver.find_elements(
            By.XPATH,
            "//button[.//i[contains(@class,'bi-chevron-right')]]"
        )

        if not next_buttons:
            break

        next_button = next_buttons[0]

        if not next_button.is_enabled():
            break

        if "disabled" in (
            next_button.get_attribute("class") or ""
        ):
            break

        previous_signature = page_signature

        next_button.click()

        # Wait until the previous page's records change
        try:
            wait.until(
                lambda d: tuple(
                    row.find_elements(
                        By.CSS_SELECTOR,
                        ".oxd-table-cell"
                    )[1].text.strip()
                    for row in d.find_elements(
                        By.CSS_SELECTOR,
                        ".oxd-table-body .oxd-table-row"
                    )
                    if len(row.find_elements(
                        By.CSS_SELECTOR,
                        ".oxd-table-cell"
                    )) >= 2
                ) != previous_signature
            )
        except TimeoutException:
            break

    # Remove duplicate IDs while preserving order
    employee_ids = list(dict.fromkeys(employee_ids))

    if not employee_ids:
        pytest.fail(
            "No employee IDs found on OrangeHRM website. "
            "Check login, employee list and table locators."
        )

    print(
        f"\nTotal employee IDs collected from UI: "
        f"{len(employee_ids)}"
    )

    print("Available Employee IDs:", employee_ids)

    return employee_ids


# --------------------------------------------------
# EMPLOYEE IDS FIXTURE
# SOURCE: ORANGEHRM WEBSITE, NOT API
# --------------------------------------------------

@pytest.fixture
def employee_ids(driver):

    login_to_orangehrm(driver)

    return fetch_employee_ids_from_ui(driver)


# --------------------------------------------------
# EMPLOYEE ID ALLOCATOR
# --------------------------------------------------

@pytest.fixture
def employee_id_allocator(employee_ids):

    available_ids = employee_ids.copy()

    random.shuffle(available_ids)

    assigned_ids = iter(available_ids)

    def get_next_employee_id():

        try:

            employee_id = next(assigned_ids)

            print(
                f"\nSelected Employee ID from UI: "
                f"{employee_id}"
            )

            return employee_id

        except StopIteration:

            pytest.fail(
                "No more employee IDs available from UI"
            )

    return get_next_employee_id


# --------------------------------------------------
# SELECT EMPLOYEE ID
# --------------------------------------------------

@pytest.fixture
def employee_id(employee_id_allocator):

    return employee_id_allocator()


# --------------------------------------------------
# FAILURE ANALYSIS HOOK
# --------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        error_message = (
            str(call.excinfo.value)
            if call.excinfo
            else "Unknown test failure"
        )

        analysis = FailureAnalyzer.analyze(
            error_message
        )

        result = {
            "test_name": item.nodeid,
            "failure_category": analysis["category"],
            "confidence": analysis["confidence"],
            "recommendation": analysis["recommendation"],
            "error_summary": analysis["error_summary"],
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        output_dir = Path("reports/ai_analysis")

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_name = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in item.name
        )

        report_path = (
            output_dir / f"{safe_name}.json"
        )

        report_path.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

        print(
            f"\nFailure analysis saved: {report_path}"
        )

        print(
            f"Classification: {analysis['category']}"
        )

        print(
            f"Recommendation: "
            f"{analysis['recommendation']}"
        )

        # Capture screenshot if browser exists
        browser_driver = item.funcargs.get("driver")

        if browser_driver:

            screenshot_dir = Path(
                "reports/screenshots"
            )

            screenshot_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            screenshot_path = (
                screenshot_dir /
                f"{safe_name}_{timestamp}.png"
            )

            browser_driver.save_screenshot(
                str(screenshot_path)
            )

            print(
                f"\nScreenshot saved: {screenshot_path}"
            )


# --------------------------------------------------
# API CLIENT FIXTURE
# --------------------------------------------------

@pytest.fixture
def api_client():

    client = APIClient()

    yield client

    client.close()
