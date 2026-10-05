import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)


@pytest.mark.smoke
def test_dashboard_loads_after_login(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed()
    assert dashboard_page.is_user_profile_displayed()