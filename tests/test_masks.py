from src.masks import mask_account, mask_card

from pytest import fixture


@fixture
def test_data():
    return "1234567890123456"


def test_mask_card(test_data) -> None:
    """
    Проверка функции mask_card() с аннотациями типов
    """
    assert mask_card(test_data) == "1234 56** **** 3456"
    assert mask_card("12345") == "Некорректный номер карты"


def test_mask_account() -> None:
    """
    Проверка функции mask_account() с аннотациями типов
    """
    assert mask_account("73654108430135874305") == "**4305"
    assert mask_account("123") == "Некорректный номер счета"
