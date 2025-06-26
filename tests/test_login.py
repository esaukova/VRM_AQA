def test_user_can_login(driver, credentials):
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.login(**credentials)
    assert "/admin" in driver.current_url, f"URL после логина: {driver.current_url}"
