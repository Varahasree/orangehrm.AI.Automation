from selenium.webdriver.common.by import By

from Framework.pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys


class AddEmployeePage(BasePage):

    ADD_EMPLOYEE_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='Add Employee']"
    )

    FIRST_NAME = (
        By.NAME,
        "firstName"
    )

    MIDDLE_NAME = (
        By.NAME,
        "middleName"
    )

    LAST_NAME = (
        By.NAME,
        "lastName"
    )

    EMPLOYEE_ID = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']"
        "/following::input[1]"
    )

    SAVE_BUTTON = (
        By.XPATH,
        "//button[@type='submit']"
    )

    REQUIRED_FIELD_ERROR = (
        By.XPATH,
        "//span[contains(@class,'oxd-input-field-error-message')]"
    )

    PERSONAL_DETAILS_HEADER = (
        By.XPATH,
        "//h6[text()='Personal Details']"
    )

    def is_add_employee_page_displayed(self):

        return self.find_element(
            self.ADD_EMPLOYEE_HEADER
        ).is_displayed()

    def enter_first_name(self, first_name):

        self.enter_text(
            self.FIRST_NAME,
            first_name
        )

    def enter_middle_name(self, middle_name):

        self.enter_text(
            self.MIDDLE_NAME,
            middle_name
        )

    def enter_last_name(self, last_name):

        self.enter_text(
            self.LAST_NAME,
            last_name
        )

    def enter_employee_id(self, employee_id):
        employee_id_element = self.find_element(self.EMPLOYEE_ID)

        # Clear the default Employee ID
        employee_id_element.click()
        employee_id_element.send_keys(
            Keys.CONTROL, "a"
        )
        employee_id_element.send_keys(Keys.BACKSPACE)

        # Enter the generated Employee ID
        employee_id_element.send_keys(str(employee_id))

        print(
            "Employee ID after entering:",
            employee_id_element.get_attribute("value")
        )
    def click_save(self):

        self.click(self.SAVE_BUTTON)

    def add_employee(
        self,
        first_name,
        last_name,
        employee_id,
        middle_name=None
    ):

        self.enter_first_name(first_name)

        if middle_name:
            self.enter_middle_name(middle_name)

        self.enter_last_name(last_name)

        self.enter_employee_id(employee_id)

        actual_id = self.find_element(
            self.EMPLOYEE_ID
        ).get_attribute("value")

        assert actual_id == str(employee_id), (
            f"Employee ID mismatch. Expected: {employee_id}, "
            f"Actual: {actual_id}"
        )

        self.click_save()

    def is_required_field_error_displayed(self):

        return self.find_element(
            self.REQUIRED_FIELD_ERROR
        ).is_displayed()