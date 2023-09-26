from selenium.webdriver.common.by import By


class CommonObjects:

    def __init__(self, driver):
        self.driver = driver

    google_searchbox = [By.XPATH,"//textarea[@name='q']"]
