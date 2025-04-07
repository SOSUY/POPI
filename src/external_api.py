import os

import requests
from dotenv import load_dotenv


def sum_transaction(transaction):
    """Функция  принимает на вход транзакцию и возвращает сумму транзакции в рублях."""
    currency = transaction["operationAmount"]["currency"]["code"]
    amount = transaction["operationAmount"]["amount"]
    if currency == "RUB":
        return amount
    else:
        load_dotenv()
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": os.getenv("API_KEY")}
        response = requests.get(url, headers=headers)
        result = response.json()
        return result["result"]
