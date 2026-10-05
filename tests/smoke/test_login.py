import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.utils.logger import get_logger
from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)


@pytest.mark.smoke
def test_valid_login(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    # Wait until OrangeHRM login page is ready
    login_page.wait_for_login_page()

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed()

@pytest.mark.parametrize(
    "username,password",
    [
        ("InvalidUser", "admin123"),
        ("Admin", "InvalidPassword"),
        ("InvalidUser", "InvalidPassword"),
    ]
)
@pytest.mark.functional
def test_invalid_login(driver, username, password):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(username, password)

    assert login_page.is_invalid_credentials_message_displayed()

    def login(self, username, password):
        logger = get_logger(__name__)

        logger.info("Entering username")
        self.enter_username(username)

        logger.info("Entering password")
        self.enter_password(password)

        logger.info("Clicking login button")
        self.click_login()