import pytest

from config.config import BASE_URL

from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage
from Framework.pages.employee_list_page import EmployeeListPage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)

from testdata.employee_data import (
    generate_employee_data
)


@pytest.mark.functional
def test_search_non_existing_employee(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    dashboard_page = DashboardPage(driver)

    dashboard_page.click_pim()


    employee_list_page = EmployeeListPage(driver)

    employee_list_page.search_employee(
        "ZZZ_NonExistingEmployee_99999"
    )

    assert (
        employee_list_page
        .is_no_records_displayed()
    )