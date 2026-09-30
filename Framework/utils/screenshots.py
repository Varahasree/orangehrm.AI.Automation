from pathlib import Path
from datetime import datetime


def capture_screenshot(driver, test_name):

    Path("reports/screenshots").mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    path = (
        f"reports/screenshots/"
        f"{test_name}_{timestamp}.png"
    )

    driver.save_screenshot(path)

    return path