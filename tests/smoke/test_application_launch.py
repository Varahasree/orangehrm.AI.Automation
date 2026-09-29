from selenium import webdriver


def test_orangehrm_application_launches():
    driver = webdriver.Chrome()

    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")
        assert "OrangeHRM" in driver.title
    finally:
        driver.quit()