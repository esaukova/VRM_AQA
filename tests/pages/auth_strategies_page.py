from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from .base_page import BasePage


class AuthStrategiesPage(BasePage):
    # Локаторы
    # Навигация
    _ACC_BTN = (By.XPATH, "//span[normalize-space()='Учётные записи']")
    _AUTH_BTN = (By.XPATH, "//span[normalize-space()='Аутентификаторы']")
    # Страница
    _CREATE_BTN = (By.XPATH, "//button[normalize-space()='Создать']")
    _DELETE_BTN = (By.XPATH, "//button[normalize-space()='Удалить']")
    _EDIT_BTN = (By.XPATH, "//button[normalize-space()='Редактировать']")
    _DATA_ROW = ("//div[@data-rowindex]"
                 "[.//div[normalize-space()='{name}'] "
                 "and .//div[normalize-space()='{comment}']]")
    # «создать / редактировать»
    _MODAL_ROOT = (By.CSS_SELECTOR, "div.DialogContent")
    _NAME_INPUT = (By.CSS_SELECTOR, "input[name='auth_name']")
    _COMMENT_INPUT = (By.CSS_SELECTOR, "input[name='comments']")
    _TYPE_FIELD = (By.ID, "mui-component-select-auth_type")
    _OPTION_TEMPLATE = "//li[@role='option' and normalize-space()='{text}']"
    _SUBMIT_BTN = (By.CSS_SELECTOR, "button[data-testid='form-drawer-submit']")
    _ERROR_NOTIFICATION = (By.CSS_SELECTOR, "div[role='alert']")
    _CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Закрыть']")
    # «удаление»
    _DELETE_BTN_MODAL = (
        By.XPATH,
        "//button[@data-testid='detail-modal-delete' and normalize-space()='Удалить']",
    )

    def __init__(self, driver, timeout: int = 10):
        super().__init__(driver, timeout)
        if "/admin/auth-strategies" not in self.driver.current_url:
            self._go_to_page()
        self.url_contains("/admin/auth-strategies")

    # Публичные методы
    def create_modal(self, name: str, comment: str,
                     auth_type: str, expect_success: bool = True):
        self.click(self._CREATE_BTN)
        self.visible(self._MODAL_ROOT)
        self._fill(name, comment, auth_type, expect_success)

    def delete_modal(self, name: str, comment: str):
        self.click(self._row_locator(name, comment))
        self.click(self._DELETE_BTN)
        self.click(self._DELETE_BTN_MODAL)

    def edit_modal(self, name: str, comment: str, name_edit: str, comment_edit: str):
        self.click(self._row_locator(name, comment))
        self.click(self._EDIT_BTN)
        self.visible(self._MODAL_ROOT)
        self._fill(name_edit, comment_edit)
        self.click(self._row_locator(name_edit, comment_edit))

    def has_strategy(self, name: str, comment: str, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self._row_locator(name, comment))
            )
            return True
        except TimeoutException:
            return False

    def is_open(self, timeout: int = 2):
        def _close():
            close_btn = self.clickable(self._CLOSE_BTN)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'})", close_btn
            )
            try:
                self.visible(self._ERROR_NOTIFICATION)
                self.is_disappeared(self._ERROR_NOTIFICATION)
            except TimeoutException:
                pass

            self.js_click(self._CLOSE_BTN)

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self._MODAL_ROOT)
            )
            return False
        except TimeoutException:
            _close()
            return True

    def wait_strategy_disappears(self, name: str, comment: str):
        self.driver_wait(self._row_locator(name, comment), EC.invisibility_of_element_located)

    # Приватные методы
    def _go_to_page(self):
        self.click(self._ACC_BTN)
        self.click(self._AUTH_BTN)

    def _row_locator(self, name: str, comment: str):
        return By.XPATH, self._DATA_ROW.format(name=name, comment=comment)

    def _fill(self, name: str, comment: str, auth_type: str = None, expect_success: bool = True):
        self.type(self._NAME_INPUT, name, clear=True)
        self.type(self._COMMENT_INPUT, comment, clear=True)
        if auth_type is not None:
            self.click(self._TYPE_FIELD)
            option = (By.XPATH, self._OPTION_TEMPLATE.format(text=auth_type))
            self.click(option)

        self.click(self._SUBMIT_BTN)
        if expect_success:
            self.is_disappeared(self._MODAL_ROOT)
