class DashboardPage:

    def __init__(self, driver):
        self.driver = driver

    def is_dashboard_displayed(self):
        return "dashboard" in self.driver.current_url.lower()