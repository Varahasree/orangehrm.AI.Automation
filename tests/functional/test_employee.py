import pytest

from config.config import BASE_URL

from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage
from Framework.pages.employee_details_page import EmployeeDetailsPage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)

from testdata.employee_data import (
    generate_employee_data
)


@pytest.mark.functional
def test_add_employee(driver):

    driver.get(BASE_URL)

    # Login
    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    # Navigate to PIM
    dashboard_page = DashboardPage(driver)

    dashboard_page.click_pim()

    pim_page = PimPage(driver)

    assert pim_page.is_pim_page_displayed()

    # Generate test data
    employee = generate_employee_data()

    # Add employee
    pim_page.click_add_employee()

    pim_page.enter_first_name(
        employee["first_name"]
    )

    pim_page.enter_last_name(
        employee["last_name"]
    )

    pim_page.save_employee()

    # Verify employee details
    details_page = EmployeeDetailsPage(driver)

    assert details_page.is_personal_details_displayed()

    assert (
        details_page.get_first_name()
        == employee["first_name"]
    )

    assert (
        details_page.get_last_name()
        == employee["last_name"]
    )