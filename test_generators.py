import pytest

from src.generators import filter_by_currency, transaction_descriptions


@pytest.fixture()
def dict_list_with_currency() -> list[dict]:
    return [
        {"id": 939719570, "operationAmount": {"currency": {"name": "USD", "code": "USD"}}},
        {"id": 142264268, "operationAmount": {"currency": {"name": "USD", "code": "USD"}}},
        {"id": 873106923, "operationAmount": {"currency": {"name": "RUB", "code": "RUB"}}},
        {"id": 895315941, "operationAmount": {"currency": {"name": "USD", "code": "USD"}}},
    ]


@pytest.fixture()
def dict_list_for_descriptions() -> list[dict]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод со счета на счет"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": "Перевод организации"},
    ]


def test_filter_by_currency(dict_list_with_currency: list[dict]) -> None:
    result = list(filter_by_currency(dict_list_with_currency, "USD"))
    assert result[0]["id"] == 939719570
    assert result[1]["id"] == 142264268


def test_transaction_descriptions(dict_list_for_descriptions: list[dict]) -> None:
    assert list(transaction_descriptions(dict_list_for_descriptions))[0] == "Перевод организации"
    assert list(transaction_descriptions(dict_list_for_descriptions))[1] == "Перевод со счета на счет"
