import csv

import pandas as pd


def transactions(file):
    """Читает CSV файл и возвращает список транзакций."""
    try:
        with open(file, encoding="utf-8") as csv_f:
            reader = csv.DictReader(csv_f, delimiter=";")
            return list(reader)
    except FileNotFoundError:
        return "Файл не найден"
    except Exception as e:
        return f"Ошибка: {e}"


def transactions_excel(file):
    """Читает Excel-файл и возвращает список транзакций."""
    try:
        df = pd.read_excel(file)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return "Файл не найден"
    except Exception as e:
        return f"Ошибка: {e}"


# print(transactions("..\\data\\transactions.csv"))
# print(transactions_excel("..\\data\\transactions_excel.xlsx"))
