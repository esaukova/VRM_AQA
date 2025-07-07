from pages.auth_strategies_page import AuthStrategiesPage
import pytest


@pytest.mark.parametrize(
    "name, comment, auth_type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_can_create(logged_driver, name, comment, auth_type):
    page = AuthStrategiesPage(logged_driver)
    page.create_modal(name=name, comment=comment, auth_type=auth_type)
    assert page.has_strategy(name, comment), "Запись не появилась в таблице"


@pytest.mark.parametrize(
    "name, comment, auth_type",
    [
        ("", "описание", "Внутренняя БД"),
        ("b" * 33, "описание", "Внутренняя БД"),
        ("     ", "описание", "Внутренняя БД"),
        ("₿€₣¥£₽¢¤¿¡§¶†‡√∫∂∑∏&≅≈∝≡≠∅", "описание", "Внутренняя БД"),
        ("阿贝非给得", "описание", "Внутренняя БД"),
    ],
)
def test_alert_create(logged_driver, name, comment, auth_type):
    page = AuthStrategiesPage(logged_driver)
    page.create_modal(name=name, comment=comment, auth_type=auth_type,expect_success=False)
    err_in_modal = page.is_open()
    if page.has_strategy(name, comment, timeout=2):
        page.delete_modal(name=name, comment=comment)
        page.wait_strategy_disappears(name, comment)
    assert err_in_modal, "Элемент был создан и не выдал ошибки"
