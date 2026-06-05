from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор принимает необязательный аргумент filename,
    который определяет, куда будут записываться логи (в файл или в консоль).
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            def write_log(message: str) -> None:
                if filename:
                    with open(filename, "a", encoding="utf-8") as log_file:
                        log_file.write(message + "\n")
                else:
                    print(message)

            write_log(f"Вызвана функция {func.__name__}")

            try:
                result = func(*args, **kwargs)
                write_log(f"{func.__name__} - OK - {result}")
                return result

            except Exception as e:
                write_log(f"{func.__name__} - {type(e).__name__} - args: {args}, kwargs: {kwargs}")

                raise

        return wrapper

    return decorator
