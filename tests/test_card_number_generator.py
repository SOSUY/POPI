import random
from typing import Any, Generator

import pytest


def card_number_generator(start: int, end: int) -> Generator[str, Any, None]:
    """
    Генератор номеров банковских карт, который должен генерировать номера карт
    в формате "XXXX XXXX XXXX XXXX", где X — цифра.
    Должны быть сгенерированы номера карт в заданном диапазоне
    """
    for i in range(start, end + 1):
        # Формируем строку из 16 случайных цифр в пределах диапазона
        card_number = ''.join(str(random.randint(0, 9)) for _ in range(16))
        # Разбиваем её на группы по 4 цифры и вставляем пробелы
        formatted_card = ' '.join([card_number[i:i + 4] for i in range(0, len(card_number), 4)])
        yield formatted_card


@pytest.fixture
def generator():
    def gen(start, end):
        return card_number_generator(start, end)

    return gen


def test_card_format(generator):
    """Проверка формата сгенерированного номера карты"""
    start = 1000
    end = 9999
    generated_cards = list(generator(start, end))

    for card in generated_cards:
        # Проверка длины строки и правильного формата
        assert len(card) == 19, f"Длина карты неверна: {card}"
        assert card.count(' ') == 3, f"Неверное количество пробелов в карте: {card}"
        parts = card.split()
        assert len(parts) == 4, f"Неверное количество частей в карте: {parts}"
        for part in parts:
            assert len(part) == 4, f"Некорректная длина части карты: {part}"


def test_randomness_of_cards(generator):
    """Проверка случайности генерации цифр в карте"""
    start = 1000
    end = 5000
    generated_cards = list(generator(start, end))
