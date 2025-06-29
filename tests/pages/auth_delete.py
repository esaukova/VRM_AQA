from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AuthDelete:
    _DELETE_BTN = (By.XPATH, "//button[@data-testid='detail-modal-delete' and normalize-space()='Удалить']")

    def __init__(self, driver, timeout=2):
        self.driver, self.wait = driver, WebDriverWait(driver, timeout)

    def delete(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN))
        btn.click()
