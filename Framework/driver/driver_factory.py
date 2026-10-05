from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:

    @staticmethod
    def create_driver(browser="chrome"):

        if browser.lower() == "chrome":

            options = Options()
            options.add_argument("--start-maximized")

            driver = webdriver.Chrome(
                options=options
            )

            return driver

        raise ValueError(
            f"Unsupported browser: {browser}"
        )