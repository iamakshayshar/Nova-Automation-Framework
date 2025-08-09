class BasePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def goto(self, path="/"):
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(url)

    def find(self, by, locator):
        return self.driver.find_element(by, locator)
