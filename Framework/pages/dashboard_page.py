from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class DashboardPage(BasePage):

    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[text()='Dashboard']"
    )

    def is_dashboard_displayed(self):
        return self.find_element(
            self.DASHBOARD_HEADER
        ).is_displayed()