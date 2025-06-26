from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
def test_user_can_transition_auth(logged_driver):
    from pages.auth_strategies import TransitionToAuth
    page = TransitionToAuth(logged_driver)
    page.windAuth()
    WebDriverWait(logged_driver, 10).until(EC.url_contains("/admin/auth-strategies"))
    assert "/admin/auth-strategies" in logged_driver.current_url, f"URL после логина: {logged_driver.current_url}"