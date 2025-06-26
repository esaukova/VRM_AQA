from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class TransitionToAuth:
    _AUTH_BTN = (By.XPATH, "//span[normalize-space()='Аутентификаторы']")
    _ACC_BTN = (By.XPATH, "//span[normalize-space()='Учётные записи']")

    def __init__(self, driver, timeout=10):
        self.driver, self.wait = driver, WebDriverWait(driver, timeout)
    def windAuth(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._ACC_BTN))
        btn.click()
        btn = self.wait.until(EC.element_to_be_clickable(self._AUTH_BTN))
        btn.click()

