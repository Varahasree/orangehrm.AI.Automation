
import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.leave_page import LeavePage
from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
)


@pytest.mark.e2e
@pytest.mark.regression
def test_user_can_open_leave_list(driver):
    driver.get(BASE_URL)

    # Step 1: Log in
    login_page = LoginPage(driver)
    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD,
    )

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dashboard_displayed()

    # Step 2: Open Leave
    dashboard_page.click_leave()

    leave_page = LeavePage(driver)
    assert leave_page.is_leave_page_displayed()

    # Step 3: Open Leave List
    leave_page.open_leave_list_tab()

    # Step 4: Verify the Leave List page
    assert leave_page.is_leave_list_displayed()

    