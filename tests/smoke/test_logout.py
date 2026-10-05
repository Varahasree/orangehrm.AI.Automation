import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.logout_page import LogoutPage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)


@pytest.mark.smoke
def test_user_can_logout(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed()

    dashboard_page.click_user_profile()

    logout_page = LogoutPage(driver)

    logout_page.click_logout()

    assert logout_page.is_login_page_displayed()