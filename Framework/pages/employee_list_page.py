from selenium.webdriver.common.by import By

from Framework.pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class EmployeeListPage(BasePage):

    EMPLOYEE_LIST_HEADER = (
        By.XPATH,
        "//h5[normalize-space()='Employee Information']"
    )

    EMPLOYEE_NAME_INPUT = (
        By.XPATH,
        "//label[text()='Employee Name']/../following-sibling::div//input"
    )

    EMPLOYEE_ID_INPUT = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']"
        "/following::input[1]"
    )

    SEARCH_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Search']"
    )

    RESET_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset']"
    )

    NO_RECORDS_MESSAGE = (
        By.XPATH,
        "//*[normalize-space()='No Records Found']"
    )

    TABLE_BODY = (
        By.XPATH,
        "//div[contains(@class,'oxd-table-body')]"
    )

    def is_employee_list_displayed(self):

        return self.find_element(
            self.EMPLOYEE_LIST_HEADER
        ).is_displayed()

    def enter_employee_name(self, employee_name):

        self.enter_text(
            self.EMPLOYEE_NAME_INPUT,
            employee_name
        )

    def enter_employee_id(self, employee_id):

        self.enter_text(
            self.EMPLOYEE_ID_INPUT,
            employee_id
        )

    def click_search(self):

        self.click(self.SEARCH_BUTTON)

    def click_reset(self):

        self.click(self.RESET_BUTTON)

    def search_employee(self, employee_name):
        self.enter_employee_name(employee_name)
        self.click(self.SEARCH_BUTTON)

        # self.enter_employee_name(
        #     employee_name
        # )
        #
        # self.click_search()

    # def is_no_records_displayed(self):
    #
    #     return self.find_element(
    #         self.NO_RECORDS_MESSAGE
    #     ).is_displayed()

    def is_no_records_displayed(self):

            no_records_locator = (
                By.XPATH,
                "//*[contains(normalize-space(), 'No Records')]"
            )

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(no_records_locator)
                )

                print("Message found:", repr(element.text))
                return True

            except TimeoutException:
                print("No records message was not found.")
                print("Current URL:", self.driver.current_url)
                print("Page title:", self.driver.title)

                search_input = self.driver.find_element(
                    *self.EMPLOYEE_NAME_INPUT
                )
                print(
                    "Search input value:",
                    search_input.get_attribute("value")
                )

                # Print text currently visible in the results area
                table = self.driver.find_elements(*self.TABLE_BODY)
                if table:
                    print("Results area text:", repr(table[0].text))

                return False
    def is_employee_table_displayed(self):

        return self.find_element(
            self.TABLE_BODY
        ).is_displayed()