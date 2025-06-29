from pages.auth_strat_page import AuthStrategiesPage
import pytest


@pytest.mark.parametrize(
    "name, comment, type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_create_delete(auth_driver, name, comment, type):
    page = AuthStrategiesPage(auth_driver)
    create_modal = page.open_create_modal()
    create_modal.fill(name=name, comment=comment, auth_type=type)
    create_modal.submit()
    delete_modal = page.delete_modal(name=name, comment=comment)
    delete_modal.delete()
    page.wait_strategy_disappears(name, comment)
