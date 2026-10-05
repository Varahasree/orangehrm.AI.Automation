from selenium.webdriver.common.by import By
from Framework.pages.base_page import BasePage


class PimPage(BasePage):

    PIM_HEADER = (
        By.XPATH,
        "//h6[text()='PIM']"
    )

    def is_pim_page_displayed(self):
        return self.find_element(
            self.PIM_HEADER
        ).is_displayed()