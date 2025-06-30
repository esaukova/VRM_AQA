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
    create_modal = page.create_modal()
    create_modal.fill(name=name, comment=comment, auth_type=auth_type)
    create_modal.submit()
    delete_modal = page.delete_modal(name=name, comment=comment)
    delete_modal.delete()
    page.wait_strategy_disappears(name, comment)
