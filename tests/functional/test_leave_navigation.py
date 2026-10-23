
import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.leave_page import LeavePage
from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
)


@pytest.mark.functional
@pytest.mark.regression
def test_open_leave_module(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD,
    )

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)
    print("Dashboard URL reached:",
          "/dashboard/index" in driver.current_url)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dashboard_displayed()

    # Navigate to Leave
    dashboard_page.click_leave()

    leave_page = LeavePage(driver)
    assert leave_page.is_leave_page_displayed()