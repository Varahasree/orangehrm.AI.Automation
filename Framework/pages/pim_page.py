from selenium.webdriver.common.by import By

from Framework.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PimPage(BasePage):

    PIM_HEADER = (
        By.XPATH,
        "//h6[text()='PIM']"
    )

    ADD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add']"
    )

    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//input[@placeholder='Type for hints...']"
    )

    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[text()='Employee Id']"
        "/following::input[1]"
    )

    FIRST_NAME_INPUT = (
        By.NAME,
        "firstName"
    )

    LAST_NAME_INPUT = (
        By.NAME,
        "lastName"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit']"
    )

    EMPLOYEE_LIST = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-body')]"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    EMPLOYEE_TABLE = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-body')]"
    )

    EMPLOYEE_LIST_MENU = (
        By.XPATH,
        "//a[contains(@href, '/pim/viewEmployeeList')]"
    )

    def is_pim_page_displayed(self):
        return self.find_element(
            self.PIM_HEADER
        ).is_displayed()

    def click_add_employee(self):
        self.click(self.ADD_BUTTON)

    def enter_first_name(self, first_name):
        self.enter_text(
            self.FIRST_NAME_INPUT,
            first_name
        )

    def enter_last_name(self, last_name):
        self.enter_text(
            self.LAST_NAME_INPUT,
            last_name
        )

    def save_employee(self):
        # Wait for the form's loading overlay to disappear
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".oxd-form-loader")
            )
        )
        # Wait until Save is clickable
        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_BUTTON)
        ).click()

    def search_employee(self, employee_name):
        self.enter_text(
            self.EMPLOYEE_NAME_INPUT,
            employee_name
        )

        self.click(self.SEARCH_BUTTON)

    def is_employee_list_displayed(self):
        return self.find_element(
            self.EMPLOYEE_TABLE
        ).is_displayed()

    def click_employee_list(self):
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_element(
                *self.EMPLOYEE_LIST_MENU
            ).click()
        )
        self.find_element(
            self.EMPLOYEE_LIST_MENU
        ).click()