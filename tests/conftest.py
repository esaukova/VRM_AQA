import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def build_driver():
    opts = Options()
    opts.add_argument("--disable-notifications")
    opts.add_argument("--start-maximized")
    prefs = {
        "profile.password_manager_leak_detection": False
    }
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    return driver


@pytest.fixture(scope="session")
def driver():
    drv = build_driver()
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def credentials():
    return {
        "user": os.getenv("TEST_USER"),
        "pwd": os.getenv("TEST_PWD"),
        "auth_name": os.getenv("TEST_AUTH")
    }


@pytest.fixture(scope="session")
def logged_driver(driver, credentials):
    from pages.login_page import LoginPage
    LoginPage(driver).login(**credentials)
    return driver
