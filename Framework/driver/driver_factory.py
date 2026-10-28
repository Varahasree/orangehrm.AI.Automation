
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:
    @staticmethod
    def create_driver(browser="chrome"):
        if browser.lower() != "chrome":
            raise ValueError(f"Unsupported browser: {browser}")

        options = Options()

        headless = (
            os.getenv("HEADLESS", "").lower() == "true"
            or os.getenv("CI", "").lower() == "true"
        )

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        return webdriver.Chrome(options=options)
