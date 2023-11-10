"""Модуль тестов"""
import re
import textwrap
from typing import Callable

import pytest
from click.testing import CliRunner
from constants import PIZZA_TYPES
from cli import bake, deliver, menu, order, pickup
from pizza_types import Margherita, Pepperoni, Pizza


@pytest.mark.parametrize(
    'method, check_log, expected_text',
    [
        (
            bake,
            False,
            """
            Готовим для Вас пиццу Pepperoni (XL)...
            Ваша пицца готова!
            """
        ),
        (
            pickup,
            False,
            """
            Ожидаем, пока Вы заберете пиццу Pepperoni (XL)...
            Приятного аппетита!
            """
        ),
        (
            deliver,
            False,
            """
            Курьер уже в пути. Везет пиццу Pepperoni (XL)...
            Приятного аппетита!
            """
        ),
        (
            bake,
            True,
            """
            Готовим для Вас пиццу Pepperoni (XL)...
            Ваша пицца готова!
            bake - за XX с!
            """
        ),
        (
            pickup,
            True,
            """
            Ожидаем, пока Вы заберете пиццу Pepperoni (XL)...
            Приятного аппетита!
            🏠 Забрали за XX с!
            """
        ),
        (
            deliver,
            True,
            """
            Курьер уже в пути. Везет пиццу Pepperoni (XL)...
            Приятного аппетита!
            🛵 Доставили за XX с!
            """
        ),
    ]
)
def test_bake_and_deliver(
    capsys,
    method: Callable,
    check_log: bool,
    expected_text: str
) -> None:
    """Тест для методов bake, deliver и pickup с декораторами и без"""
    pizza = Pepperoni('XL')
    has_decorator = hasattr(method, '__wrapped__')
    if not check_log and has_decorator:
        method = method.__wrapped__  # type: ignore
    method(pizza)
    captured = capsys.readouterr()
    output = captured.out.strip()
    replaced_output = re.sub(r'за \d{1,2} с!', 'за XX с!', output)
    expected_output = textwrap.dedent(expected_text).strip()
    assert replaced_output == expected_output


@pytest.mark.parametrize(
    'pizza_type, size, delivery, expected_text',
    [
        (
            'Pepperoni',
            'XL',
            False,
            'Ожидаем, пока Вы заберете пиццу Pepperoni (XL)'
        ),
        (
            'Pepperoni',
            '',
            True,
            'Курьер уже в пути. Везет пиццу Pepperoni (L)'
        ),
        ('Cheese', 'L', True, 'Такой пиццы нет в меню'),
        ('Pepperoni', 'S', True, 'У нас есть только следующие размеры'),
    ]
)
def test_order(
    pizza_type: str,
    size: str,
    delivery: bool,
    expected_text: str
) -> None:
    """Тест для метода order с различными параметрами"""
    runner = CliRunner()
    params = [pizza_type]
    if delivery:
        params.append('--delivery')
    if size:
        params.extend(['--size', size])
    result = runner.invoke(order, params)
    assert result.exit_code == 0
    assert expected_text in result.output


def test_menu() -> None:
    """Тест для метода order с различными параметрами"""
    runner = CliRunner()
    result = runner.invoke(menu, [])
    assert result.exit_code == 0
    assert 'МЕНЮ' in result.output
    for pizza_type in PIZZA_TYPES:
        assert pizza_type in result.output


@pytest.mark.parametrize(
    'first_pizza, second_pizza, result',
    [
        (Pepperoni('XL'), Pepperoni('L'), False),
        (Margherita('XL'), Pepperoni('L'), False),
        (Pepperoni('XL'), Pepperoni('XL'), True),
        (Pepperoni('XL'), 'string', False),
    ]
)
def test_pizza_equality(first_pizza, second_pizza, result):
    """Тест для сравнения пицц"""
    assert (first_pizza == second_pizza) == result


def test_wrong_pizza_size():
    """Тест для проверки ошибки при создании пиццы неверного размера"""
    with pytest.raises(ValueError):
        Pepperoni('S')


def test_wrong_pizza_recipe():
    """Тест для проверки ошибки при получении ингридиентов"""
    with pytest.raises(ValueError):
        Pizza('XL').dict()
