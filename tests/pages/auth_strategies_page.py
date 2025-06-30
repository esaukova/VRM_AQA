from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AuthStrategiesPage:
    _ACC_BTN = (By.XPATH, "//span[normalize-space()='Учётные записи']")
    _AUTH_BTN = (By.XPATH, "//span[normalize-space()='Аутентификаторы']")

    _CREATE_BTN = (By.XPATH, "//button[normalize-space()='Создать']")
    _DELETE_BTN = (By.XPATH, "//button[normalize-space()='Удалить']")
    _DATA_ROW = "//div[@data-rowindex][.//div[normalize-space()='{name}'] and .//div[normalize-space()='{comment}']]"

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        if "/admin/auth-strategies" not in driver.current_url:
            self._go_to_page()
        self.wait.until(EC.url_contains("/admin/auth-strategies"))

    def create_modal(self):
        self.driver.find_element(*self._CREATE_BTN).click()
        return self.AuthCreate(self.driver)

    def delete_modal(self, name: str, comment: str):
        self.wait.until(EC.element_to_be_clickable(self._row_locator(name, comment))).click()
        self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN)).click()
        return self.AuthDelete(self.driver)

    def _go_to_page(self):
        self.wait.until(EC.element_to_be_clickable(self._ACC_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self._AUTH_BTN)).click()

    def _row_locator(self, name: str, comment: str):
        return By.XPATH, self._DATA_ROW.format(name=name, comment=comment)

    def has_strategy(self, name: str, comment: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self._row_locator(name, comment))
            )
            return True
        except TimeoutException:
            return False

    def wait_strategy_disappears(self, name: str, comment: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self._row_locator(name, comment))
        )

    class AuthCreate:
        _MODAL_ROOT = (By.CSS_SELECTOR, "div.DialogContent")
        _NAME_INPUT = (By.CSS_SELECTOR, "input[name='auth_name']")
        _COMMENT_INPUT = (By.CSS_SELECTOR, "input[name='comments']")
        _TYPE_FIELD = (By.ID, "mui-component-select-auth_type")
        _OPTION_TEMPLATE = "//li[@role='option' and normalize-space()='{text}']"
        _SUBMIT_BTN = (By.CSS_SELECTOR, "button[data-testid='form-drawer-submit']")
        _ERROR_NOTIFICATION = (By.CSS_SELECTOR, "div[role='alert']")

        def __init__(self, driver, timeout: int = 10):
            self.driver = driver
            self.wait = WebDriverWait(driver, timeout)
            self.modal = self.wait.until(EC.visibility_of_element_located(self._MODAL_ROOT))

        def fill(self, name: str, comment: str, auth_type: str):
            self.modal.find_element(*self._NAME_INPUT).send_keys(name)
            self.modal.find_element(*self._COMMENT_INPUT).send_keys(comment)
            self.modal.find_element(*self._TYPE_FIELD).click()
            option = (By.XPATH, self._OPTION_TEMPLATE.format(text=auth_type))
            self.wait.until(EC.element_to_be_clickable(option)).click()

        def submit(self, expect_success: bool = True):
            self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()
            if expect_success:
                self.wait.until(EC.invisibility_of_element_located(self._MODAL_ROOT))

        def is_open(self):
            def _close(timeout: int = 10):
                wait = WebDriverWait(self.driver, timeout)
                close_btn = wait.until(EC.element_to_be_clickable(self._CLOSE_BTN))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'})", close_btn
                )
                try:
                    WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located(self._ERROR_NOTIFICATION)
                    )
                    wait.until(EC.invisibility_of_element_located(self._ERROR_NOTIFICATION))
                    close_btn.click()
                except TimeoutException:
                    self.driver.execute_script("arguments[0].click()", close_btn)

            try:
                opened = self.modal.is_displayed()
                _close()
            except StaleElementReferenceException:
                opened = False
            return opened

    class AuthDelete:
        _DELETE_BTN = (By.XPATH, "//button[@data-testid='detail-modal-delete' and normalize-space()='Удалить']")

        def __init__(self, driver, timeout: int = 2):
            self.driver = driver
            self.wait = WebDriverWait(driver, timeout)

        def delete(self):
            self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN)).click()
