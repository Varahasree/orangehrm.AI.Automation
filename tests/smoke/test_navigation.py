import pytest

from config.config import BASE_URL
from Framework.pages.login_page import LoginPage
from Framework.pages.dashboard_page import DashboardPage
from Framework.pages.pim_page import PimPage

from testdata.login_data import (
    VALID_USERNAME,
    VALID_PASSWORD
)


@pytest.mark.smoke
def test_navigate_to_pim(driver):

    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    login_page.login(
        VALID_USERNAME,
        VALID_PASSWORD
    )

    dashboard_page = DashboardPage(driver)

    assert dashboard_page.is_dashboard_displayed()

    dashboard_page.click_pim()

    pim_page = PimPage(driver)

    assert pim_page.is_pim_page_displayed()