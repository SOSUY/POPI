import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("api_key")


def read_transactions(file_path: Path) -> List[Dict[str, Any]]:
    """Считывает транзакции из JSON-файла."""
    try:
        with file_path.open(encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_transaction_rub(currency: str) -> Any:
    """Получает курс валюты от API и возвращает его в виде float"""
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    try:
        response = requests.get(url, headers={"apikey": API_KEY}, timeout=5)
        response.raise_for_status()
        """Поднимает исключение, если код ответа не 2xx"""
        response_data = response.json()
        rate = response_data["rates"]["RUB"]
        return rate
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {e}")
        """# Возвращаем 1.0 как значение по умолчанию"""
        return 1.0


def sum_amount(transactions: List[dict]) -> float:
    """Суммирует суммы всех транзакций"""
    total = 0.0
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_code = operation_amount.get("currency", {}).get("code")
        amount = float(operation_amount.get("amount", 0))
        if currency_code == "RUB":
            total += amount
        elif currency_code in ("EUR", "USD"):
            rate = get_transaction_rub(currency_code)
            total += amount * rate
        else:
            print(f"Неизвестная валюта: {currency_code}")
    return total


if __name__ == "__main__":
    operations_path = Path("../data/operations.json")
    transactions = read_transactions(operations_path)
    total_rub = sum_amount(transactions)
    print(f"Общая сумма в рублях: {total_rub:.2f}")
