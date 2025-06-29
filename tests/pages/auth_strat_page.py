from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tests.pages.auth_create import AuthCreate
from tests.pages.auth_delete import AuthDelete


class AuthStrategiesPage:
    _CREATE_BTN = (By.XPATH, "//button[normalize-space()='Создать']")
    _DELETE_BTN = (By.XPATH, "//button[normalize-space()='Удалить']")
    _DATA_ROW = "//div[@data-rowindex][.//div[normalize-space()='{name}'] and .//div[normalize-space()='{comment}']]"

    def __init__(self, driver, timeout: int = 5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.wait.until(EC.url_contains("/admin/auth-strategies"))

    def open_create_modal(self):
        self.driver.find_element(*self._CREATE_BTN).click()
        return AuthCreate(self.driver)

    def delete_modal(self, name: str, comment: str):
        row = self.wait.until(EC.element_to_be_clickable(self.row_locator(name, comment)))
        row.click()
        delete_btn = self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN))
        delete_btn.click()
        return AuthDelete(self.driver)

    def row_locator(self, name: str, comment: str):
        return By.XPATH, self._DATA_ROW.format(name=name, comment=comment)

    def wait_strategy_disappears(self, name: str, comment: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(self.row_locator(name, comment)))

    def has_strategy(self, name: str, comment: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.row_locator(name=name, comment=comment)))
            return True
        except TimeoutException:
            return False
