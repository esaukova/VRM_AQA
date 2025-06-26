from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.pages.license import LicenseModal
class LoginPage:
    URL = "http://192.168.1.65/auth"
    _USER = (By.NAME, "name")
    _PASS = (By.NAME, "password")
    _AUTH = (By.ID, "mui-component-select-authStrategyId")
    _SUBMIT = (By.CSS_SELECTOR, "button[data-cy='login-submit']")
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    def open(self):
        self.driver.get(self.URL)
    def set_username(self, value: str):
        self.wait.until(EC.visibility_of_element_located(self._USER)).send_keys(value)
    def set_password(self, value: str):
        self.driver.find_element(*self._PASS).send_keys(value)
    def choose_authenticator(self, text: str):
        self.wait.until(EC.element_to_be_clickable(self._AUTH)).click()
        option = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, f"//li[@role='option' and normalize-space()='{text}']")))
        self.driver.execute_script("arguments[0].click()", option)
    def submit(self):
        self.wait.until(EC.element_to_be_clickable(self._SUBMIT)).click()
    def login(self, user, pwd, auth_name):
        self.open()
        self.set_username(user)
        self.set_password(pwd)
        self.choose_authenticator(auth_name)
        self.submit()
        LicenseModal(self.driver, timeout=5).accept()
