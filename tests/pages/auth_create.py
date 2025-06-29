from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AuthCreate:
    _MODAL_ROOT = (By.CSS_SELECTOR, "div.DialogContent")
    _NAME_INPUT = (By.CSS_SELECTOR, "input[name='auth_name']")
    _COMMENT_INPUT = (By.CSS_SELECTOR, "input[name='comments']")
    _TYPE_FIELD = (By.ID, "mui-component-select-auth_type")
    _OPTION_TEMPLATE = "//li[@role='option' and normalize-space()='{text}']"
    _SUBMIT_BTN = (By.CSS_SELECTOR, "button[data-testid='form-drawer-submit']")
    _ERROR_NOTIFICATION = (By.CSS_SELECTOR, "div[role='alert']")
    _FIELD_ERROR = (By.CSS_SELECTOR, "span.[normalize-space()='Обязательное поле']")
    _CLOSE_BTN = (By.CSS_SELECTOR, "button[aria-label='Закрыть']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.modal = self.wait.until(EC.visibility_of_element_located(self._MODAL_ROOT))

    def fill(self, name, comment: str, auth_type: str):
        self.modal.find_element(*self._NAME_INPUT).send_keys(str(name))
        self.modal.find_element(*self._COMMENT_INPUT).send_keys(comment)
        self.modal.find_element(*self._TYPE_FIELD).click()
        option = (By.XPATH, self._OPTION_TEMPLATE.format(text=auth_type))
        self.wait.until(EC.element_to_be_clickable(option)).click()

    def submit(self, expect_success: bool = True):
        self.wait.until(EC.element_to_be_clickable(self._SUBMIT_BTN)).click()
        if expect_success:
            self.wait.until(EC.invisibility_of_element_located(self._MODAL_ROOT))

    def is_open(self):
        try:
            opened = self.modal.is_displayed()
            self.close()
        except StaleElementReferenceException:
            opened = False
        return opened

    def close(self, timeout: int = 10):
        wait = WebDriverWait(self.driver, timeout)
        close_btn = wait.until(EC.element_to_be_clickable(self._CLOSE_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'})", close_btn)
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(self._ERROR_NOTIFICATION))
            wait.until(EC.invisibility_of_element_located(self._ERROR_NOTIFICATION))
            close_btn.click()
        except TimeoutException:
            self.driver.execute_script("arguments[0].click()", close_btn)
