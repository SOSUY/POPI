import json
import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests
from dotenv import load_dotenv

from src.utils import get_transaction_rub, read_transactions

load_dotenv()
API_KEY = os.getenv("api_key")


@pytest.fixture(scope='session', autouse=True)
def remove_temp_files():
    yield
    for filename in ['test_transactions.json']:
        if os.path.exists(filename):
            os.remove(filename)


@patch('requests.get')
def test_get_transaction_rub_api_error(mock_get: Mock) -> None:
    """Тестируем поведение функции при ошибке API."""
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mock_get.return_value = mock_response

    result = get_transaction_rub('USD')
    assert result == 1.0


def test_read_transactions_success() -> None:
    """Тест успешного чтения файла с транзакциями."""
    test_data = [{'amount': 100, 'currency': 'RUB'}]
    with open('test_transactions.json', 'w') as f:
        json.dump(test_data, f)

    result = read_transactions(Path('test_transactions.json'))
    assert result == test_data


def test_read_transactions_empty_file() -> None:
    """Тест чтения пустого файла."""
    with open('test_transactions.json', 'w'):
        pass

    result = read_transactions(Path('test_transactions.json'))
    assert result == []
