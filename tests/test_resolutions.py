import pytest
from pages.resolutions_page import ResolutionsPage

@pytest.mark.positive
def test_create_resolution_success(logged_driver):
    """
    Тест: Успешное создание нового разрешения.
    """
    page = ResolutionsPage(logged_driver)
    modal = page.open_create_modal()
    resolution_name = "Test Resolution"
    modal.fill_form(name=resolution_name, login="test_user", password="123")
    modal.submit()
    assert page.has_resolution_in_table(resolution_name), f"Разрешение '{resolution_name}' не появилось в таблице"

@pytest.mark.negative
def test_create_resolution_empty_name_fails(logged_driver):
    """
    Тест: Попытка создать разрешение с пустым именем.
    Ожидается, что окно закроется, а запись в таблице не появится.
    """
    page = ResolutionsPage(logged_driver)
    modal = page.open_create_modal()
    modal.fill_form(name="", login="user", password="pwd")
    modal.submit() # Пытаемся нажать 'Создать'
    # Закрываем окно (если оно не закрылось само)
    if not modal.is_closed():
        modal.close()
    # Проверяем, что разрешение с пустым именем не было создано
    assert not page.has_resolution_in_table(name=""), "Разрешение с пустым именем было создано, хотя не должно было"

@pytest.mark.negative
def test_cancel_resolution_creation(logged_driver):
    """
    Тест: Отмена создания разрешения.
    """
    page = ResolutionsPage(logged_driver)
    modal = page.open_create_modal()
    resolution_name = "Cancelled Resolution"
    modal.fill_form(name=resolution_name, login="cancel_user", password="password123")
    modal.close()
    assert modal.is_closed(), "Модальное окно не закрылось после отмены"
    assert not page.has_resolution_in_table(resolution_name), "Разрешение было создано после отмены"

@pytest.mark.positive
def test_show_hide_password_button(logged_driver):
    """
    Тест: Проверка работы кнопки видимости пароля.
    """
    page = ResolutionsPage(logged_driver)
    modal = page.open_create_modal()
    
    # 1. Вводим пароль и проверяем, что поле имеет тип 'password'
    modal.fill_form(password="SuperSecret123")
    assert modal.get_password_input_type() == "password", "Изначально поле пароля имеет неверный тип"
    
    # 2. Нажимаем на 'глаз' и проверяем, что тип поля изменился на 'text'
    modal.toggle_password_visibility()
    assert modal.get_password_input_type() == "text", "Тип поля не изменился на 'text' после клика"
    
    # 3. Нажимаем на 'глаз' еще раз и проверяем, что тип вернулся на 'password'
    modal.toggle_password_visibility()
    assert modal.get_password_input_type() == "password", "Тип поля не вернулся на 'password' после второго клика"