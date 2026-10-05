from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class LogoutPage(BasePage):

    LOGOUT_BUTTON = (
        By.XPATH,
        "//a[text()='Logout']"
    )

    USERNAME_FIELD = (
        By.NAME,
        "username"
    )

    def click_logout(self):
        self.click(self.LOGOUT_BUTTON)

    def is_login_page_displayed(self):
        return self.find_element(
            self.USERNAME_FIELD
        ).is_displayed()