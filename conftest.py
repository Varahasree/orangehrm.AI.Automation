import pytest

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