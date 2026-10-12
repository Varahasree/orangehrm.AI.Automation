from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class LoginPage(BasePage):

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    INVALID_CREDENTIALS_MESSAGE = (
        By.XPATH,
        "//p[contains(@class,'oxd-alert-content-text') and text()='Invalid credentials']"
    )

    def wait_for_login_page(self):
        self.find_element(self.USERNAME)

    def enter_username(self, username):
        self.enter_text(self.USERNAME, username)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def is_invalid_credentials_message_displayed(self):
        return self.find_element(
            self.INVALID_CREDENTIALS_MESSAGE
        ).is_displayed()