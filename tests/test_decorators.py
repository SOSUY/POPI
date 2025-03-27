import os
import pytest
from unittest.mock import patch
import datetime  # Добавили импорт datetime

from decorators import log  # Предположим, что декоратор находится в модуле 'decorators.py'


@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Очистка файлов после каждого теста
    for filename in ["test_log_1.txt", "test_log_2.txt", "test_log_3.txt"]:
        if os.path.exists(filename):
            os.remove(filename)


def test_decorator_with_file_logging():
    @log(filename="test_log_1.txt")
    def add_numbers(x, y):
        return x + y

    add_numbers(10, 20)

    # Проверяем содержимое файла
    with open("test_log_1.txt", "r") as file:
        lines = file.readlines()
        assert len(lines) == 1
        expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} add_numbers ok\n"
        assert lines[0].startswith(expected_output[:26])  # Первые 26 символов включают дату и время до секунд


def test_decorator_without_file_logging(capsys):
    @log()
    def subtract_numbers(x, y):
        return x - y

    subtract_numbers(30, 15)

    captured = capsys.readouterr()
    expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} subtract_numbers ok\n"
    assert captured.out.startswith(expected_output[:26])


def test_decorator_with_exception(capsys):
    @log(filename="test_log_2.txt")
    def divide_numbers(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    # Проверяем содержимое файла
    with open("test_log_2.txt", "r") as file:
        lines = file.readlines()
        assert len(lines) == 1
        expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} divide_numbers error: ZeroDivisionError. Inputs: (10, 0), {}\n"
        assert lines[0].startswith(expected_output[:26])


# Дополнительные тесты

def test_decorator_with_no_arguments(capsys):
    @log()
    def greet():
        print("Hello, World!")

    greet()

    captured = capsys.readouterr()
    expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} greet ok\n"
    assert captured.out.startswith(expected_output[:26])


def test_decorator_with_keyword_arguments(capsys):
    @log()
    def calculate_area(width=10, height=20):
        return width * height

    calculate_area(height=30, width=40)

    captured = capsys.readouterr()
    expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} calculate_area ok\n"
    assert captured.out.startswith(expected_output[:26])


def test_decorator_with_nested_calls(capsys):
    @log()
    def inner_function():
        pass

    @log()
    def outer_function():
        inner_function()

    outer_function()

    captured = capsys.readouterr()
    expected_output_inner = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} inner_function ok\n"
    expected_output_outer = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} outer_function ok\n"
    assert expected_output_inner in captured.out
    assert expected_output_outer in captured.out


def test_decorator_with_multiple_args_and_kwargs(capsys):
    @log()
    def complex_operation(a, b, c=3, d=4):
        return a + b + c + d

    complex_operation(1, 2, d=6)

    captured = capsys.readouterr()
    expected_output = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} complex_operation ok\n"
    assert captured.out.startswith(expected_output[:26])
