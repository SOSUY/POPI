import datetime
import functools
from typing import Any, Callable


def log(filename: str = None) -> Callable:
    """
    Декоратор для логирования вызова функции и её результата.

    :param filename: (опционально) Имя файла для записи логов.
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
                log_message = (
                    f"{timestamp} {func.__name__} error: "
                    f"{type(e).__name__}. Inputs: {args}, {kwargs}"
                )

            if filename:
                with open(filename, "a") as file:
                    file.write(log_message + "\n")
            else:
                print(log_message)

            return result

        return wrapper

    return decorator


# Примеры использования

@log(filename="mylog.txt")
def my_function(x: int, y: int) -> int:
    """Пример простой функции для тестирования декоратора."""
    return x + y


if __name__ == "__main__":
    my_function(1, 2)  # Логирование будет выполняться в файл 'mylog.txt'
