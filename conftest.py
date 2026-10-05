import pytest
from pathlib import Path
from datetime import datetime
from Framework.driver.driver_factory import DriverFactory


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