import json
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8", mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def json_transactions(way):
    """Функция принимает на вход путь до JSON-файла и возвращает список
    словарей с данными о финансовых транзакциях."""
    try:
        with open(way, encoding="utf-8") as f:
            data = json.load(f)
            if data == "" or type(data) != list:
                logger.critical("Неправильный формат JSON-файла")
                return []
            else:
                logger.info(f"Функция закончила выполнение со значениями: {data}")
                return data
    except Exception as ex:
        logger.critical(f"Ошибка. Тип ошибки:  {ex}")
        return []


# print(json_transactions("../data/operations.json"))
