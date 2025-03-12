import datetime
import functools
from typing import Any, Callable


def log(filename: Any = None) -> Callable:
    """
    Декоратор для логирования вызова функции и ее результата.
    Args:
        filename: (опционально) Имя файла для записи логов.
                   Если не указано, логи выводятся в консоль.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} {func.__name__} ok"
            except Exception as e:
                result = None
                log_message = f"{timestamp} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"

            if filename:
                with open(filename, "a") as f:
                    f.write(log_message + "\n")
            else:
                print(log_message)
            return result

        return wrapper

    return decorator


# Как это работает:
#
# 1. log(filename=None):
#    - Внешняя функция декоратора.
#    - filename: опциональный аргумент для имени файла лога.
#
# 2. decorator(func):
#    - Внутренняя функция декоратора, которая принимает декорируемую функцию func.
#
# 3. wrapper(*args, **kwargs):
#    - Обертка, которая будет вызываться вместо оригинальной функции.
#    - Записывает текущее время.
#    - Блок try...except:
#    - Пытается выполнить оригинальную функцию func.
#    - Если успешен, формирует сообщение об успехе.
#    - Если возникла ошибка, формирует сообщение об ошибке с типом ошибки и входными параметрами.
#
# 4. Запись лога:
#    - Если filename указан, открывает файл в режиме добавления ("a") и записывает сообщение.
#    - Иначе, выводит сообщение в консоль.
#
# 5. Возврат результата:
#    - Возвращает результат выполнения оригинальной функции (или None, если была ошибка).


@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    return x + y


my_function(1, 2)  # Вывод в файл mylog.txt