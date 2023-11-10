"""Декораторы для функций"""
from functools import wraps
from random import randint
from typing import Callable, Optional


def log(pattern: Optional[str] = None) -> Callable:
    """Вывод рандомного времени выполнения для метода"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            func(*args, **kwargs)
            duration = randint(1, 60)
            if pattern:
                print(pattern.format(duration))
            else:
                print(f'{func.__name__} - за {duration} с!')
        return wrapper
    return decorator
