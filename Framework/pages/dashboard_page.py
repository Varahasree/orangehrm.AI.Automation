from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class DashboardPage(BasePage):

    DASHBOARD_HEADER = (
        By.XPATH,
        "//h6[text()='Dashboard']"
    )

    USER_PROFILE = (
        By.XPATH,
        "//span[contains(@class, 'oxd-userdropdown-tab')]"
    )

    PIM_MENU = (
        By.XPATH,
        "//span[text()='PIM']"
    )
    LEAVE_MENU = (
        By.XPATH,
        "//span[normalize-space()='Leave']"
    )

    def is_dashboard_displayed(self):
        return self.find_element(
            self.DASHBOARD_HEADER
        ).is_displayed()

    def is_user_profile_displayed(self):
        return self.find_element(
            self.USER_PROFILE
        ).is_displayed()

    def click_pim(self):
        self.click(self.PIM_MENU)

    def click_user_profile(self):
        self.click(self.USER_PROFILE)

    def click_leave(self):
        self.click(self.LEAVE_MENU)