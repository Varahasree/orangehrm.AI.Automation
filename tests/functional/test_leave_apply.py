
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
def test_open_leave_apply_form(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD,
    )

    dashboard_page = DashboardPage(driver)
    dashboard_page.click_leave()

    leave_page = LeavePage(driver)
    assert leave_page.is_leave_page_displayed()

    leave_page.open_apply_tab()

    assert leave_page.is_apply_page_displayed()