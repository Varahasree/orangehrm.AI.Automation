
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LocatorHealer:
    """
    Tries a primary locator, followed by explicitly approved
    fallback locators.

    This is rule-based recovery, not an AI model. A future
    AI component may suggest fallback locators, but those
    suggestions must be validated before use.
    """

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.recovery_log = []

    def find_element(self, primary_locator, fallbacks=None):
        fallbacks = fallbacks or []

        candidates = [
            ("primary", primary_locator),
            *[
                (f"fallback_{index}", locator)
                for index, locator in enumerate(
                    fallbacks, start=1
                )
            ],
        ]

        for source, locator in candidates:
            try:
                element = WebDriverWait(
                    self.driver,
                    self.timeout,
                ).until(
                    EC.visibility_of_element_located(locator)
                )

                self.recovery_log.append({
                    "source": source,
                    "locator": str(locator),
                    "success": True,
                })

                return element

            except (
                NoSuchElementException,
                TimeoutException,
            ):
                self.recovery_log.append({
                    "source": source,
                    "locator": str(locator),
                    "success": False,
                })

        raise NoSuchElementException(
            "Primary locator and all approved fallbacks failed."
        )
