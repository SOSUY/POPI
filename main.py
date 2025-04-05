from src.bank_operations import re_sort
from src.finance_tracker import transactions, transactions_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import json_transactions
from src.widget import get_date, mask_account_card


def main():
    """Это основная функция, которая обрабатывает вводы пользователя и дает корректный результат."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print(
        """Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла"""
    )
    while True:
        user_input = input()
        if user_input == "1":
            print("Для обработки выбран JSON-файл.")
            file_name = 1
            trans = json_transactions("data/operations.json")
            break
        elif user_input == "2":
            print("Для обработки выбран CSV-файл.")
            file_name = 2
            trans = transactions("data/transactions.csv")
            break
        elif user_input == "3":
            print("Для обработки выбран XLSX-файл.")
            file_name = 2
            trans = transactions_excel("data/transactions_excel.xlsx")
            break
        else:
            print("Такого выбора нет.")
    while True:
        user_input = input(
            """Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтрации статусы: EXECUTED, CANCELED, PENDING
"""
        ).upper()
        if user_input in ["EXECUTED", "CANCELED", "PENDING"]:
            trans = filter_by_state(trans, user_input)
            break
        else:
            print(f"Статус операции {user_input} недоступен.")

    while True:
        print("Отсортировать операции по дате? Да/Нет")
        user_input = input().lower()
        if user_input == "да":
            sort_date = True
            break
        elif user_input == "нет":
            sort_date = False
            break
        else:
            print("Нет такого ответа.")

    if sort_date:
        while True:
            print("Отсортировать по возрастанию или по убыванию? ")
            user_input = input().lower()
            if user_input == "по возрастанию":
                trans = sort_by_date(trans, False)
                break
            elif user_input == "по убыванию":
                trans = sort_by_date(trans, True)
                break
            else:
                print("Нет такого ответа.")
    while True:
        print("Выводить только рублевые транзакции? Да/Нет")
        user_input = input().lower()
        if user_input == "да":
            trans = list(filter_by_currency(trans, "RUB"))
            break
        elif user_input == "нет":
            break
        else:
            print("Нет такого ответа.")
    while True:
        print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
        user_input = input().lower()
        if user_input == "да":
            user_input = input("Введите слово: \n")
            trans = re_sort(trans, user_input)
            break
        elif user_input == "нет":
            break
        else:
            print("Нет такого ответа.")

    print("Распечатываю итоговый список транзакций...")
    if len(trans):
        print(f"Всего банковских операций в выборке: {len(trans)}\n")
        for date in trans:
            ye_mo_da = get_date(date.get("date"))
            desc = date.get("description")
            if date.get("description") == "Открытие вклада":
                mask_disc = mask_account_card(date.get("to"))
            else:
                mask_card = mask_account_card(date.get("from"))
                mask_disc = mask_account_card(date.get("to"))
            if file_name == 1:
                op_am = date.get("operationAmount")
                summa = f"Сумма: {op_am.get("amount")} {op_am.get("currency").get("name")}"
            elif file_name == 2:
                summa = f"Сумма: {date.get("amount")} {date.get("currency_code")}"
            if date.get("description") == "Открытие вклада":
                print(f"{ye_mo_da} {desc}\n" f"{mask_disc}\n" f"{summa}\n")
            else:
                print(f"{ye_mo_da} {desc}\n" f"{mask_card} -> {mask_disc}\n" f"{summa}\n")

    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


main()