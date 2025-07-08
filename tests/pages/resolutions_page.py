from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ResolutionsPage:
    # --- Локаторы для навигации ---
    _SETTINGS_BTN = (By.XPATH, "//span[normalize-space()='Настройки']")
    _RESOLUTIONS_BTN = (By.XPATH, "//span[normalize-space()='Разрешения']")
    _MAIN_DELETE_BTN = (By.CSS_SELECTOR, "button[data-cy='table-delete']")
    _CONFIRM_DELETE_BTN = (By.CSS_SELECTOR, "button[data-testid='detail-modal-delete']")
    _FIRST_ROW_CHECKBOX = (By.CSS_SELECTOR, "div[data-rowindex='0'] input[type='checkbox']")
    _ALL_ROWS = (By.CSS_SELECTOR, "div.MuiDataGrid-row")
    _DATA_ROW_TEMPLATE = "//div[@role='row' and .//div[text()='{name}']]"
    # --- Локаторы основной страницы ---
    _CREATE_BTN = (By.XPATH, "//button[normalize-space()='Создать']")
    _DATA_ROW_TEMPLATE = "//div[@role='row' and .//div[text()='{name}']]"

    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        if "/admin/templates" not in driver.current_url:
            self._go_to_page()
        self.wait.until(EC.url_contains("/admin/templates"))

    def _go_to_page(self):
        self.wait.until(EC.element_to_be_clickable(self._SETTINGS_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self._RESOLUTIONS_BTN)).click()

    def open_create_modal(self):
        create_button = self.wait.until(EC.presence_of_element_located(self._CREATE_BTN))
        self.driver.execute_script("arguments[0].click();", create_button)
        return self.CreateResolutionModal(self.driver, self.wait)
    def delete_all_resolutions(self):
        """Удаляет все разрешения со страницы, пока они не закончатся."""
        while True:
            try:
                # Проверяем, есть ли хоть одна строка, с коротким ожиданием
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(self._ALL_ROWS))
                # Кликаем на первый чекбокс
                self.wait.until(EC.element_to_be_clickable(self._FIRST_ROW_CHECKBOX)).click()
                # Нажимаем основную кнопку 'Удалить'
                self.wait.until(EC.element_to_be_clickable(self._MAIN_DELETE_BTN)).click()
                # В окне подтверждения нажимаем 'Удалить'
                self.wait.until(EC.element_to_be_clickable(self._CONFIRM_DELETE_BTN)).click()
                # Ждем немного, чтобы таблица успела обновиться
                time.sleep(1)
            except TimeoutException:
                # Если строк больше нет, выходим из цикла
                break
    def has_resolution_in_table(self, name: str) -> bool:
        try:
            row_locator = (By.XPATH, self._DATA_ROW_TEMPLATE.format(name=name))
            self.wait.until(EC.visibility_of_element_located(row_locator))
            return True
        except TimeoutException:
            return False

    # Расположен внутри класса ResolutionsPage в файле pages/resolutions_page.py

    class CreateResolutionModal:
        # ... (остальные локаторы остаются без изменений)
        _NAME_INPUT = (By.CSS_SELECTOR, "[data-cy='name'] input")
        _PORT_INPUT = (By.CSS_SELECTOR, "[data-cy='port'] input")
        _LOGIN_INPUT = (By.CSS_SELECTOR, "[data-cy='login'] input")
        _PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-cy='password'] input")
        _WIDTH_INPUT = (By.CSS_SELECTOR, "[data-cy='width'] input")
        _HEIGHT_INPUT = (By.CSS_SELECTOR, "[data-cy='height'] input")
        _MODAL_ROOT = (By.CSS_SELECTOR, "div[data-testid='form-drawer']")
        # ИСПРАВЛЕНО: Правильный локатор для кнопки 'Закрыть' (крестик)
        _CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Закрыть']")
        _ERROR_MESSAGE = (By.CSS_SELECTOR, "p.Mui-error")
        _SUBMIT_BTN = (By.CSS_SELECTOR, "[data-testid='form-drawer-submit']")
        _PASSWORD_VISIBILITY_TOGGLE = (By.CSS_SELECTOR, "[data-cy='password'] button")

        def __init__(self, driver, wait):
            self.driver = driver
            self.wait = wait

        # Метод fill_form остается без изменений
        def fill_form(self, name=None, port=None, login=None, password=None, width=None, height=None):
            if name is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._NAME_INPUT))
                field.clear()
                field.send_keys(name)
            if port is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._PORT_INPUT))
                field.clear()
                field.send_keys(port)
            if login is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._LOGIN_INPUT))
                field.clear()
                field.send_keys(login)
            if password is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._PASSWORD_INPUT))
                field.clear()
                field.send_keys(password)
            if width is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._WIDTH_INPUT))
                field.clear()
                field.send_keys(width)
            if height is not None:
                field = self.wait.until(EC.visibility_of_element_located(self._HEIGHT_INPUT))
                field.clear()
                field.send_keys(height)

        def submit(self):
            self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()

        def get_error_text(self) -> str:
            # Этот метод нам больше не нужен для теста с пустым именем, но пусть останется для других проверок
            try:
                error_wait = WebDriverWait(self.driver, 3)
                return error_wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE)).text
            except TimeoutException:
                return ""
        
        # ДОБАВЛЕНО: Новый метод для проверки состояния кнопки
        def is_submit_button_enabled(self) -> bool:
            """Проверяет, активна ли кнопка 'Создать'."""
            submit_button = self.wait.until(EC.presence_of_element_located(self._SUBMIT_BTN))
            return submit_button.is_enabled()

        def close(self):
            self.wait.until(EC.element_to_be_clickable(self._CLOSE_BTN)).click()

        def is_closed(self, timeout: int = 5) -> bool:
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located(self._MODAL_ROOT)
                )
            except TimeoutException:
                return False
    
        def toggle_password_visibility(self):
            """Нажимает на иконку 'глаза' для показа/скрытия пароля."""
            self.wait.until(EC.element_to_be_clickable(self._PASSWORD_VISIBILITY_TOGGLE)).click()

        def get_password_input_type(self) -> str:
            """Возвращает тип поля для ввода пароля ('password' или 'text')."""
            return self.wait.until(EC.presence_of_element_located(self._PASSWORD_INPUT)).get_attribute("type")

        def submit(self):
            self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()

        def close(self):
            self.wait.until(EC.element_to_be_clickable(self._CLOSE_BTN)).click()

        def is_closed(self, timeout: int = 5) -> bool:
            try:
                return WebDriverWait(self.driver, timeout).until(
                    EC.invisibility_of_element_located(self._MODAL_ROOT))
            except TimeoutException:
                return False