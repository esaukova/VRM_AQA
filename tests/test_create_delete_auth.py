from pages.auth_strategies_page import AuthStrategiesPage
import pytest


@pytest.mark.parametrize(
    "name, comment, auth_type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_create_delete(logged_driver, name, comment, auth_type):
    page = AuthStrategiesPage(logged_driver)
    page.create_modal(name=name, comment=comment, auth_type=auth_type)
    page.delete_modal(name=name, comment=comment)
    page.wait_strategy_disappears(name, comment)
