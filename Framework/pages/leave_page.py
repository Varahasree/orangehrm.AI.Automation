
from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class LeavePage(BasePage):
    LEAVE_HEADER = (
        By.XPATH,
        "//h6[normalize-space()='Leave']"
    )

    APPLY_TAB = (
        By.XPATH,
        "//a[normalize-space()='Apply']"
    )

    MY_LEAVE_TAB = (
        By.XPATH,
        "//a[normalize-space()='My Leave']"
    )

    LEAVE_LIST_TAB = (
        By.XPATH,
        "//a[normalize-space()='Leave List']"
    )
    LEAVE_LIST_HEADER = (
        By.XPATH,
        "//h5[normalize-space()='Leave List']"
    )

    APPLY_HEADER = (
        By.XPATH,
        "//*[self::h5 or self::h6 or self::div]"
        "[normalize-space()='Apply Leave']"
    )

    def is_leave_page_displayed(self):
        return self.find_element(
            self.LEAVE_HEADER
        ).is_displayed()

    def open_apply_tab(self):
        self.click(self.APPLY_TAB)

    def open_my_leave_tab(self):
        self.click(self.MY_LEAVE_TAB)

    def open_leave_list_tab(self):
        self.click(self.LEAVE_LIST_TAB)

    def is_leave_list_displayed(self):
        return self.find_element(
            self.LEAVE_LIST_HEADER
        ).is_displayed()

    def is_apply_page_displayed(self):
        return self.find_element(
            self.APPLY_HEADER
        ).is_displayed()

