import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage

@pytest.mark.smoke
def test_valid_login(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(
        "Admin",
        "admin123"
    )

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed()