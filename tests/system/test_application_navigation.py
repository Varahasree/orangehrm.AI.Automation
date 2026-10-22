
import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage
from Framework.pages.leave_page import LeavePage
from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
)


@pytest.mark.system
@pytest.mark.regression
def test_user_can_navigate_between_pim_and_leave(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dashboard_displayed()

    # Verify PIM
    dashboard_page.click_pim()

    pim_page = PimPage(driver)
    assert pim_page.is_pim_page_displayed()

    # Navigate to Leave
    dashboard_page.click_leave()

    leave_page = LeavePage(driver)
    assert leave_page.is_leave_page_displayed()
