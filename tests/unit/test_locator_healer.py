
from unittest.mock import Mock

import pytest
from selenium.common.exceptions import TimeoutException

from Framework.ai.locator_healer import LocatorHealer


def test_primary_locator_succeeds_without_fallback():
    driver = Mock()
    expected_element = Mock()

    healer = LocatorHealer(driver)

    # Mock the wait condition to return an element.
    from unittest.mock import patch

    with patch(
        "Framework.ai.locator_healer.WebDriverWait"
    ) as wait_class:
        wait_class.return_value.until.return_value = (
            expected_element
        )

        element = healer.find_element(
            ("id", "username"),
            [("name", "username")],
        )

    assert element is expected_element
    assert healer.recovery_log[0]["source"] == "primary"
    assert healer.recovery_log[0]["success"] is True


def test_fallback_locator_succeeds():
    driver = Mock()
    expected_element = Mock()

    healer = LocatorHealer(driver)

    from unittest.mock import patch

    with patch(
        "Framework.ai.locator_healer.WebDriverWait"
    ) as wait_class:
        wait_instance = wait_class.return_value
        wait_instance.until.side_effect = [
            TimeoutException("Primary locator not found"),
            expected_element,
        ]

        element = healer.find_element(
            ("id", "old-username"),
            [("name", "username")],
        )

    assert element is expected_element
    assert healer.recovery_log[0]["success"] is False
    assert healer.recovery_log[1]["source"] == "fallback_1"
    assert healer.recovery_log[1]["success"] is True


def test_all_locators_fail():
    driver = Mock()
    healer = LocatorHealer(driver)

    from unittest.mock import patch

    with patch(
        "Framework.ai.locator_healer.WebDriverWait"
    ) as wait_class:
        wait_class.return_value.until.side_effect = (
            TimeoutException("Element not found")
        )

        with pytest.raises(
            Exception,
            match="all approved fallbacks failed",
        ):
            healer.find_element(
                ("id", "missing"),
                [("name", "missing")],
            )
