import pytest
from pages.auth_strat_page import AuthStrategiesPage


@pytest.mark.parametrize(
    "name, comment, type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_can_delete(auth_driver, name, comment, type):
    page = AuthStrategiesPage(auth_driver)
    delete_modal = page.delete_modal(name=name, comment=comment)
    delete_modal.delete()
    page.wait_strategy_disappears(name, comment)
    assert not page.has_strategy(name, comment), "Запись все еще в таблице в таблице"
