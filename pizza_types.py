"""Модуль с классами пицц"""
from constants import PIZZA_SIZES
from typing import List, Union


class Pizza:
    """Базовый класс для пицц"""

    def __init__(self, size: str) -> None:
        if size not in PIZZA_SIZES:
            raise ValueError(f'Извините, мы готовим только {PIZZA_SIZES}')
        self.size: str = size
        self.name: str = ''
        self.emoji: str = ''
        self.recipe: List[str] = []

    def __eq__(self, other):
        if issubclass(type(other), Pizza):
            return self.size == other.size and self.name == other.name
        return False

    def dict(self):
        """Метод для получения рецепта пиццы"""
        if not self.name:
            raise ValueError('Сначала нужно выбрать тип пиццы!')
        return {f'{self.emoji} {self.name}': self.recipe}


class Margherita(Pizza):
    """Класс для пиццы Маргарита"""

    def __init__(self, size: str) -> None:
        super().__init__(size)
        self.emoji = '🧀'
        self.name = 'Margherita'
        self.recipe = ['tomato sauce', 'mozzarella', 'tomatoes']


class Pepperoni(Pizza):
    """Класс для пиццы Пепперони"""

    def __init__(self, size: str) -> None:
        super().__init__(size)
        self.emoji = '🍕'
        self.name = 'Pepperoni'
        self.recipe = ['tomato sauce', 'mozzarella', 'pepperoni']


class Hawaiian(Pizza):
    """Класс для пиццы Гавайская"""

    def __init__(self, size: str) -> None:
        super().__init__(size)
        self.emoji = '🍍'
        self.name = 'Hawaiian'
        self.recipe = ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']


PizzaType = Union[Margherita, Pepperoni, Hawaiian]
