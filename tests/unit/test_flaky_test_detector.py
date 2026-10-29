
import pytest

from Framework.ai.flaky_test_detector import FlakyTestDetector


@pytest.mark.unit
def test_detects_mixed_pass_and_fail_results():
    results = [
        {"test": "test_login", "outcome": "passed"},
        {"test": "test_login", "outcome": "failed"},
        {"test": "test_login", "outcome": "passed"},
    ]

    report = FlakyTestDetector.analyze_results(results)

    assert report["test_login"]["potentially_flaky"] is True
    assert report["test_login"]["passed"] == 2
    assert report["test_login"]["failed"] == 1


@pytest.mark.unit
def test_consistently_passing_test_is_not_flagged():
    results = [
        {"test": "test_dashboard", "outcome": "passed"},
        {"test": "test_dashboard", "outcome": "passed"},
    ]

    report = FlakyTestDetector.analyze_results(results)

    assert report["test_dashboard"]["potentially_flaky"] is False


@pytest.mark.unit
def test_skipped_only_test_is_not_flagged_as_flaky():
    results = [
        {"test": "test_api", "outcome": "skipped"},
        {"test": "test_api", "outcome": "skipped"},
    ]

    report = FlakyTestDetector.analyze_results(results)

    assert report["test_api"]["potentially_flaky"] is False


@pytest.mark.unit
def test_empty_results_return_empty_report():
    assert FlakyTestDetector.analyze_results([]) == {}
