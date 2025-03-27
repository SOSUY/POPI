import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.apilayer.com/exchangerates_data/convert"

    def convert(self, from_currency, to_currency, amount):
        headers = {'apikey': self.api_key}
        params = {'from': from_currency, 'to': to_currency, 'amount': amount}

        response = requests.get(self.base_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        converted_amount = data['result']
        logging.info(f"{amount} {from_currency} = {converted_amount} {to_currency}")
        return converted_amount


if __name__ == "__main__":
    converter = CurrencyConverter(api_key="YOUR_API_KEY_HERE")
    print(converter.convert("EUR", "USD", 100))
