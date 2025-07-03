from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class AuthStrategiesPage:
    # Локаторы для перехода
    _ACC_BTN = (By.XPATH, "//span[normalize-space()='Учётные записи']")
    _AUTH_BTN = (By.XPATH, "//span[normalize-space()='Аутентификаторы']")
    # Локаторы страницы аутентификаторов
    _CREATE_BTN = (By.XPATH, "//button[normalize-space()='Создать']")
    _DELETE_BTN = (By.XPATH, "//button[normalize-space()='Удалить']")
    _EDIT_BTN = (By.XPATH, "//button[normalize-space()='Редактировать']")
    _DATA_ROW = "//div[@data-rowindex][.//div[normalize-space()='{name}'] and .//div[normalize-space()='{comment}']]"
    # Локаторы окна создания и редактирования
    _MODAL_ROOT = (By.CSS_SELECTOR, "div.DialogContent")
    _NAME_INPUT = (By.CSS_SELECTOR, "input[name='auth_name']")
    _COMMENT_INPUT = (By.CSS_SELECTOR, "input[name='comments']")
    _TYPE_FIELD = (By.ID, "mui-component-select-auth_type")
    _OPTION_TEMPLATE = "//li[@role='option' and normalize-space()='{text}']"
    _SUBMIT_BTN = (By.CSS_SELECTOR, "button[data-testid='form-drawer-submit']")
    _ERROR_NOTIFICATION = (By.CSS_SELECTOR, "div[role='alert']")
    _CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Закрыть']")
    # Локаторы окна удаления
    _DELETE_BTN_MODAL = (By.XPATH, "//button[@data-testid='detail-modal-delete' and normalize-space()='Удалить']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        if "/admin/auth-strategies" not in driver.current_url:
            self._go_to_page()
        self.wait.until(EC.url_contains("/admin/auth-strategies"))

    # Публичные методы
    def create_modal(self, name: str, comment: str, auth_type: str, expect_success: bool = True):
        self.driver.find_element(*self._CREATE_BTN).click()
        modal = self.wait.until(EC.visibility_of_element_located(self._MODAL_ROOT))
        self._fill(modal, name, comment, auth_type, expect_success)

    def delete_modal(self, name: str, comment: str):
        self.wait.until(EC.element_to_be_clickable(self._row_locator(name, comment))).click()
        self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self._DELETE_BTN_MODAL)).click()

    def edit_modal(self, name: str, comment: str, name_edit: str, comment_edit: str):
        self.wait.until(EC.element_to_be_clickable(self._row_locator(name, comment))).click()
        self.wait.until(EC.element_to_be_clickable(self._EDIT_BTN)).click()
        modal = self.wait.until(EC.visibility_of_element_located(self._MODAL_ROOT))
        self._fill(modal, name_edit, comment_edit)
        self.wait.until(EC.element_to_be_clickable(self._row_locator(name_edit, comment_edit))).click()

    def has_strategy(self, name: str, comment: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self._row_locator(name, comment))
            )
            return True
        except TimeoutException:
            return False

    def is_open(self, timeout: int = 2):
        def _close(close_timeout: int = 10):
            wait = WebDriverWait(self.driver, close_timeout)
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
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self._MODAL_ROOT)
            )
            opened = False
        except TimeoutException:
            opened = True
            _close()
        return opened

    def wait_strategy_disappears(self, name: str, comment: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self._row_locator(name, comment))
        )

    # Приватные методы
    def _go_to_page(self):
        self.wait.until(EC.element_to_be_clickable(self._ACC_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self._AUTH_BTN)).click()

    def _row_locator(self, name: str, comment: str):
        return By.XPATH, self._DATA_ROW.format(name=name, comment=comment)

    def _fill(self, modal, name: str, comment: str, auth_type: str = None, expect_success: bool = True):
        def submit():
            self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()
            if expect_success:
                self.wait.until(EC.invisibility_of_element_located(self._MODAL_ROOT))

        name_input = self.wait.until(
            EC.element_to_be_clickable(self._NAME_INPUT)
        )
        name_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        name_input.send_keys(name)
        comment_input = self.wait.until(
            EC.element_to_be_clickable(self._COMMENT_INPUT)
        )
        comment_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        comment_input.send_keys(comment)
        if auth_type is not None:
            modal.find_element(*self._TYPE_FIELD).click()
            option = (By.XPATH, self._OPTION_TEMPLATE.format(text=auth_type))
            self.wait.until(EC.element_to_be_clickable(option)).click()
        submit()
