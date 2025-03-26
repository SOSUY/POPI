import json
import os
from pathlib import Path
from unittest.mock import Mock, patch

"""# Импортируем Mock и patch для создания заглушек"""

import requests
from dotenv import load_dotenv

from src.utils import get_transaction_rub, read_transactions

load_dotenv()
API_KEY = os.getenv("api_key")


"""# Тест функции get_transaction_rub при ошибке API"""


@patch("requests.get")  # Заменяем функцию requests.get заглушкой
def test_get_transaction_rub_api_error(mock_get: Mock) -> None:
    """# Создаем заглушку ответа, которая будет вызывать исключение при проверке статуса"""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mock_get.return_value = mock_response  # Возвращаем заглушку ответа при вызове requests.get

    # Проверяем, что функция возвращает 1.0 при ошибке API
    result = get_transaction_rub("USD")
    assert result == 1.0


"""# Тест функции read_transactions при успешном чтении файла"""


def test_read_transactions_success() -> None:
    # Создаем тестовые данные для записи в файл
    test_data = [{"amount": 100, "currency": "RUB"}]
    with open("test_transactions.json", "w") as f:
        json.dump(test_data, f)  # Записываем тестовые данные в JSON файл

    """# Проверяем, что функция возвращает правильный список транзакций"""
    result = read_transactions(Path("test_transactions.json"))
    assert result == test_data

    os.remove("test_transactions.json")  # Удаляем тестовый файл


"""# Тест функции read_transactions при чтении пустого файла"""


def test_read_transactions_empty_file() -> None:
    # Создаем пустой файл
    with open("test_transactions.json", "w") as f:
        pass

    """# Проверяем, что функция возвращает пустой список"""
    result = read_transactions(Path("test_transactions.json"))
    assert result == []

    os.remove("test_transactions.json")  # Удаляем тестовый файл
