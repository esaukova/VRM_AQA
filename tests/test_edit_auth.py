from pages.auth_strategies_page import AuthStrategiesPage
import pytest


@pytest.mark.parametrize(

    "name, comment, auth_type, name_edit, comment_edit",
    [
        ("до", "до", "Внутренняя БД", "после", "после"),
    ],
)
def test_user_create_delete(logged_driver, name, comment, auth_type, name_edit, comment_edit):
    page = AuthStrategiesPage(logged_driver)
    page.create_modal(name=name, comment=comment, auth_type=auth_type)
    page.edit_modal(name=name, comment=comment, name_edit=name_edit, comment_edit=comment_edit)
    page.delete_modal(name=name_edit, comment=comment_edit)
    page.wait_strategy_disappears(name_edit, comment_edit)
