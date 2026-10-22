import pytest
from Framework.driver.driver_factory import DriverFactory
from Framework.api.api_client import APIClient
import json
from pathlib import Path
from datetime import datetime, timezone

from Framework.ai.failure_analyzer import FailureAnalyzer



def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on"
    )


@pytest.fixture
def driver(request):

    browser = request.config.getoption("--browser")

    driver = DriverFactory.create_driver(browser)

    yield driver

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        error_message = str(
            call.excinfo.value
        ) if call.excinfo else "Unknown test failure"

        analysis = FailureAnalyzer.analyze(error_message)

        result = {
            "test_name": item.nodeid,
            "failure_category": analysis["category"],
            "confidence": analysis["confidence"],
            "recommendation": analysis["recommendation"],
            "error_summary": analysis["error_summary"],
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        output_dir = Path("reports/ai_analysis")
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_name = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in item.name
        )

        report_path = output_dir / f"{safe_name}.json"
        report_path.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

        print(f"\nFailure analysis saved: {report_path}")
        print(f"Classification: {analysis['category']}")
        print(f"Recommendation: {analysis['recommendation']}")

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver")

        if driver:

            Path("reports/screenshots").mkdir(
                parents=True,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            test_name = item.name

            screenshot_path = (
                f"reports/screenshots/"
                f"{test_name}_{timestamp}.png"
            )

            driver.save_screenshot(screenshot_path)

            print(
                f"\nScreenshot saved: "
                f"{screenshot_path}"
    )

@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()