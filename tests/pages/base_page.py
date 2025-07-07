from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys


class BasePage:

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _wait(self, locator, condition):
        return self.wait.until(condition(locator))

    def driver_wait(self, locator, condition, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(condition(locator))

    def open(self, url: str):
        self.driver.get(url)

    def find(self, locator):
        return self._wait(locator, EC.presence_of_element_located)

    def visible(self, locator):
        return self._wait(locator, EC.visibility_of_element_located)

    def click(self, locator):
        self._wait(locator, EC.element_to_be_clickable).click()

    def clickable(self, locator):
        return self._wait(locator, EC.element_to_be_clickable)

    def presence_click(self, locator):
        self._wait(locator, EC.presence_of_element_located).click()

    def js_click(self, locator):
        element = self.visible(locator)
        self.driver.execute_script("arguments[0].click()", element)

    def type(self, locator, text: str, clear: bool = False):
        element = self.visible(locator)
        if clear:
            element.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        element.send_keys(text)

    def is_disappeared(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def url_contains(self, substring: str):
        return self.wait.until(EC.url_contains(substring))
