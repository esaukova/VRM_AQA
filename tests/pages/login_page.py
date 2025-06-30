from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "http://192.168.1.65/auth"
    _USER = (By.NAME, "name")
    _PASS = (By.NAME, "password")
    _AUTH = (By.ID, "mui-component-select-authStrategyId")
    _SUBMIT = (By.CSS_SELECTOR, "button[data-cy='login-submit']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def login(self, user, pwd, auth_name):
        self._open()
        self._set_username(user)
        self._set_password(pwd)
        self._choose_authenticator(auth_name)
        self._submit()
        self.LicenseModal(self.driver, timeout=5).accept()

    def _open(self):
        self.driver.get(self.URL)

    def _set_username(self, value: str):
        self.wait.until(EC.visibility_of_element_located(self._USER)).send_keys(value)

    def _set_password(self, value: str):
        self.driver.find_element(*self._PASS).send_keys(value)

    def _choose_authenticator(self, text: str):
        self.wait.until(EC.element_to_be_clickable(self._AUTH)).click()
        option = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//li[@role='option' and normalize-space()='{text}']")))
        self.driver.execute_script("arguments[0].click()", option)

    def _submit(self):
        self.wait.until(EC.element_to_be_clickable(self._SUBMIT)).click()

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
