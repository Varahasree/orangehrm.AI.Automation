
import pytest

from Framework.ai.failure_analyzer import FailureAnalyzer


@pytest.mark.parametrize(
    "error_message, expected_category",
    [
        (
            "selenium.common.exceptions.TimeoutException",
            "timeout",
        ),
        (
            "selenium.common.exceptions.NoSuchElementException",
            "locator_issue",
        ),
        (
            "AssertionError: expected Dashboard",
            "assertion_failure",
        ),
        (
            "requests.exceptions.ConnectionError",
            "api_error",
        ),
        (
            "Unexpected browser crash",
            "unknown",
        ),
    ],
)
def test_failure_classification(
    error_message,
    expected_category,
):
    result = FailureAnalyzer.analyze(error_message)

    assert result["category"] == expected_category
    assert result["recommendation"]
    assert result["error_summary"]
