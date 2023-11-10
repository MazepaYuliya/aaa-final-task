"""Модуль с консольными командами"""
from time import sleep

import click
import pizza_types
from constants import PIZZA_SIZES, PIZZA_TYPES
from decorators import log
from pizza_types import PizzaType


def get_menu_text() -> str:
    """Метод для получения текста меню"""
    text = 'МЕНЮ:\n'
    for pizza_type in PIZZA_TYPES:
        pizza = getattr(pizza_types, pizza_type)
        text += f'{pizza("L").dict()}\n'
    return text


@click.group()
def cli() -> None:
    """Самая вкусная пицца только у нас!"""


@cli.command()
def menu() -> None:
    """Наше меню"""
    print(get_menu_text())


@log()
def bake(pizza: PizzaType) -> None:
    """Готовит пиццу"""
    print(f'Готовим для Вас пиццу {pizza.name} ({pizza.size})...')
    sleep(2)
    print('Ваша пицца готова!')


@log('🛵 Доставили за {} с!')
def deliver(pizza: PizzaType) -> None:
    """Доставка"""
    print(f'Курьер уже в пути. Везет пиццу {pizza.name} ({pizza.size})...')
    sleep(2)
    print('Приятного аппетита!')


@log('🏠 Забрали за {} с!')
def pickup(pizza: PizzaType) -> None:
    """Самовывоз"""
    print(f'Ожидаем, пока Вы заберете пиццу {pizza.name} ({pizza.size})...')
    sleep(2)
    print('Приятного аппетита!')


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', default='L', is_flag=False)
@click.argument('pizza_type', nargs=1)
def order(pizza_type: str, size: str, delivery: bool) -> None:
    """Сделать заказ"""
    if pizza_type not in PIZZA_TYPES:
        print('Такой пиццы нет в меню')
        print(get_menu_text())
        return

    if size not in PIZZA_SIZES:
        print(f'У нас есть только следующие размеры: {PIZZA_SIZES}')
        print(get_menu_text())
        return

    pizza_obj = getattr(pizza_types, pizza_type)(size=size)
    bake(pizza_obj)
    if delivery:
        deliver(pizza_obj)
    else:
        pickup(pizza_obj)


if __name__ == '__main__':
    cli()
