import pytest

from config.config import BASE_URL

from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage
from Framework.pages.add_employee_page import AddEmployeePage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)


@pytest.mark.functional
def test_add_employee_required_fields(driver):

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

    # Open Add Employee
    pim_page.click_add_employee()

    add_employee_page = AddEmployeePage(driver)

    assert (
        add_employee_page
        .is_add_employee_page_displayed()
    )

    # Save without entering mandatory data
    add_employee_page.click_save()

    # Verify validation
    assert (
        add_employee_page
        .is_required_field_error_displayed()
    )