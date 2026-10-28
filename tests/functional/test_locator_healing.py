
from selenium.webdriver.common.by import By

from config.config import BASE_URL
from Framework.ai.locator_healer import LocatorHealer


def test_username_field_can_be_found_with_fallback(driver):
    driver.get(BASE_URL)

    healer = LocatorHealer(driver, timeout=10)

    element = healer.find_element(
        (By.ID, "intentionally-outdated-locator"),
        [(By.NAME, "username")],
    )

    assert element.is_displayed()
    assert element.is_enabled()

    assert healer.recovery_log[0]["success"] is False
    assert healer.recovery_log[1]["success"] is True
