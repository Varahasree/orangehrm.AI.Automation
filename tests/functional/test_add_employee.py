import pytest

from config.config import BASE_URL

from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage
from Framework.pages.add_employee_page import AddEmployeePage
from Framework.pages.employee_details_page import EmployeeDetailsPage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)

from testdata.employee_data import (
    generate_employee_data
)


@pytest.mark.functional
@pytest.mark.regression
def test_add_employee(driver):

    driver.get(BASE_URL)

    # Login
    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    # Open PIM
    dashboard_page = DashboardPage(driver)

    dashboard_page.click_pim()

    pim_page = PimPage(driver)

    assert pim_page.is_pim_page_displayed()

    # Open Add Employee
    pim_page.click_add_employee()

    add_employee_page = AddEmployeePage(driver)

    assert (
        add_employee_page
        .is_add_employee_page_displayed()
    )

    # Generate test data
    employee = generate_employee_data()

    # Create employee
    add_employee_page.add_employee(
        first_name=employee["first_name"],
        last_name=employee["last_name"]
    )

    # Verify employee details page
    employee_details_page = EmployeeDetailsPage(driver)

    assert (
        employee_details_page
        .is_personal_details_displayed()
    )

    assert (
        employee_details_page.get_first_name()
        == employee["first_name"]
    )

    assert (
        employee_details_page.get_last_name()
        == employee["last_name"]
    )