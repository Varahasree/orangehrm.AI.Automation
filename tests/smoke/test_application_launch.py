from config.config import BASE_URL


def test_orangehrm_application_launches(driver):

    driver.get(BASE_URL)

    assert "OrangeHRM" in driver.title