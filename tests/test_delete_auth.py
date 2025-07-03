import pytest
from pages.auth_strategies_page import AuthStrategiesPage


@pytest.mark.parametrize(
    "name, comment, auth_type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_can_delete(logged_driver, name, comment, auth_type):
    page = AuthStrategiesPage(logged_driver)
    page.delete_modal(name=name, comment=comment)
    page.wait_strategy_disappears(name, comment)
    assert not page.has_strategy(name, comment), "Запись все еще в таблице в таблице"
