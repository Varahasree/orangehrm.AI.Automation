from selenium.webdriver.common.by import By

from Framework.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EmployeeDetailsPage(BasePage):

    PERSONAL_DETAILS_HEADER = (
        By.XPATH,
        "//h6[text()='Personal Details']"
    )

    FIRST_NAME_INPUT = (
        By.XPATH,
        "//input[@name='firstName']"
    )

    LAST_NAME_INPUT = (
        By.XPATH,
        "//input[@name='lastName']"
    )

    MIDDLE_NAME = (
        By.NAME,
        "middleName"
    )

    def is_personal_details_displayed(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *self.PERSONAL_DETAILS_HEADER
        ).is_displayed()
        )
        return self.find_element(
            self.PERSONAL_DETAILS_HEADER
        ).is_displayed()

    def get_first_name(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *self.FIRST_NAME_INPUT
            ).get_attribute("value") != ""
        )

        return self.find_element(
            self.FIRST_NAME_INPUT
        ).get_attribute("value")

    def get_last_name(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *self.LAST_NAME_INPUT
            ).get_attribute("value") != ""
        )

        return self.find_element(
            self.LAST_NAME_INPUT
        ).get_attribute("value")

    def get_middle_name(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *self.MIDDLE_NAME
            ).get_attribute("value") != ""
        )