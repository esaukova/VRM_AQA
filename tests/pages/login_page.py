from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    URL = "http://192.168.1.65/auth"
    _USER = (By.NAME, "name")
    _PASS = (By.NAME, "password")
    _AUTH = (By.ID, "mui-component-select-authStrategyId")
    _SUBMIT = (By.CSS_SELECTOR, "button[data-cy='login-submit']")
    _TITLE = (By.XPATH, "//h2[normalize-space()='Лицензионное соглашение']")
    _CHECK_INPUT = (By.CSS_SELECTOR, "input.PrivateSwitchBase-input")
    _CONTINUE_BTN = (By.XPATH, "//button[normalize-space()='Продолжить']")

    def login(self, user: str, pwd: str, auth_name: str):
        self.open(self.URL)
        self.type(self._USER, user)
        self.type(self._PASS, pwd)
        self._choose_authenticator(auth_name)
        self.click(self._SUBMIT)
        self._accept()

    def _choose_authenticator(self, text: str):
        self.click(self._AUTH)
        option = (By.XPATH,
                  f"//li[@role='option' and normalize-space()='{text}']")
        self.js_click(option)

    def _accept(self):
        self.visible(self._TITLE)
        self.presence_click(self._CHECK_INPUT)
        self.click(self._CONTINUE_BTN)
        self.is_disappeared(self._TITLE)
