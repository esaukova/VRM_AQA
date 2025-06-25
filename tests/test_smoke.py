import importlib
import pytest

@pytest.mark.parametrize(
    "pkg_name",
    [
        "selenium",
        "pytest",
        "webdriver_manager"
    ],
)
def test_package_importable(pkg_name):
    try:
        importlib.import_module(pkg_name)
    except ModuleNotFoundError as exc:
        pytest.fail(f"Не удалось импортировать {pkg_name}: {exc}")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture(scope="session")
def browser():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


def test_example_com_title(browser):
    browser.get("https://example.com")
    assert "example" in browser.title.lower(), "Неверный title страницы"


def test_search_input_available(browser):
    browser.get("https://google.com")
    search_box = browser.find_element(By.NAME, "q")
    assert search_box.is_displayed()
