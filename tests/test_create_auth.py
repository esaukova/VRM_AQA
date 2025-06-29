from pages.auth_strat_page import AuthStrategiesPage
import pytest


@pytest.mark.parametrize(
    "name, comment, type",
    [
        ("название", "описание", "Внутренняя БД"),
        ("название", "", "Внутренняя БД"),
    ],
)
def test_user_can_create(auth_driver, name, comment, type):
    page = AuthStrategiesPage(auth_driver)
    modal = page.open_create_modal()
    modal.fill(name=name, comment=comment, auth_type=type)
    modal.submit()
    assert page.has_strategy(name, comment), "Запись не появилась в таблице"


@pytest.mark.parametrize(
    "name, comment, type",
    [
        ("", "описание", "Внутренняя БД"),
        ("b" * 33, "описание", "Внутренняя БД"),
        ("     ", "описание", "Внутренняя БД"),
        ("₿€₣¥£₽¢¤¿¡§¶†‡√∫∂∑∏&≅≈∝≡≠∅", "описание", "Внутренняя БД"),
        ("阿贝非给得", "описание", "Внутренняя БД"),
    ],
)
def test_alert_create(auth_driver, name, comment, type):
    page = AuthStrategiesPage(auth_driver)
    modal = page.open_create_modal()
    modal.fill(name=name, comment=comment, auth_type=type)
    modal.submit(expect_success=False)
    err_in_modal = modal.is_open()
    if page.has_strategy(name, comment, timeout=2):
        delete_modal = page.delete_modal(name=name, comment=comment)
        delete_modal.delete()
        page.wait_strategy_disappears(name, comment)
    assert err_in_modal, "Элемент был создан и не выдал ошибки"
