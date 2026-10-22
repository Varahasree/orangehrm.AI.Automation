
import re


class FailureAnalyzer:
    RULES = [
        {
            "category": "timeout",
            "patterns": [
                r"TimeoutException",
                r"timed out",
                r"TimeoutError",
            ],
            "recommendation": (
                "Check page loading, explicit waits, "
                "and whether the expected element exists."
            ),
        },
        {
            "category": "locator_issue",
            "patterns": [
                r"NoSuchElementException",
                r"Unable to locate element",
                r"no such element",
            ],
            "recommendation": (
                "Inspect the current DOM and verify "
                "the locator and page state."
            ),
        },
        {
            "category": "assertion_failure",
            "patterns": [
                r"AssertionError",
                r"assert .*==",
                r"assert .* is True",
            ],
            "recommendation": (
                "Compare expected and actual values "
                "and confirm the test data and behavior."
            ),
        },
        {
            "category": "api_error",
            "patterns": [
                r"HTTPError",
                r"ConnectionError",
                r"requests.exceptions",
                r"status_code.*(4\d\d|5\d\d)",
            ],
            "recommendation": (
                "Check the endpoint, response status, "
                "authentication, and service availability."
            ),
        },
    ]

    @classmethod
    def analyze(cls, error_message):
        message = str(error_message)

        for rule in cls.RULES:
            if any(
                re.search(pattern, message, re.IGNORECASE)
                for pattern in rule["patterns"]
            ):
                return {
                    "category": rule["category"],
                    "confidence": "high",
                    "recommendation": rule["recommendation"],
                    "error_summary": message[:500],
                }

        return {
            "category": "unknown",
            "confidence": "low",
            "recommendation": (
                "Review the traceback, screenshot, logs, "
                "and application state manually."
            ),
            "error_summary": message[:500],
        }
