from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class LicenseModal:
    _TITLE = (By.XPATH, "//h2[normalize-space()='Лицензионное соглашение']")
    _CHECK_INPUT = (By.CSS_SELECTOR, "input.PrivateSwitchBase-input")
    _CONTINUE_BTN = (By.XPATH, "//button[normalize-space()='Продолжить']")
    def __init__(self, driver, timeout=10):
        self.driver, self.wait = driver, WebDriverWait(driver, timeout)
    def accept(self):
        self.wait.until(EC.visibility_of_element_located(self._TITLE))
        btn = self.wait.until(EC.presence_of_element_located(self._CHECK_INPUT))
        btn.click()
        btn = self.wait.until(EC.element_to_be_clickable(self._CONTINUE_BTN))
        btn.click()
        self.wait.until(EC.invisibility_of_element_located(self._TITLE))
