from selenium.webdriver.common.by import By

from Framework.utils.waits import Waits


class LoginPage:

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = Waits(driver)

    def enter_username(self, username):

        element = self.wait.element_visible(
            self.USERNAME
        )

        element.clear()
        element.send_keys(username)

    def enter_password(self, password):

        element = self.wait.element_visible(
            self.PASSWORD
        )

        element.clear()
        element.send_keys(password)

    def click_login(self):

        self.wait.element_clickable(
            self.LOGIN_BUTTON
        ).click()

    def login(self, username, password):

        self.enter_username(username)
        self.enter_password(password)
        self.click_login()