# coding: utf-8
import pytest
from decouple import Choices


FRUIT_APPLE = 'apple'
FRUIT_BANANA = 'banana'
FRUIT_COCONUT = 'coconut'

ALLOWED_FRUITS = (
        (FRUIT_APPLE, 'Apple'),
        (FRUIT_BANANA, 'Banana'),
        (FRUIT_COCONUT, 'Coconut'),
    )

ZERO = 0
THREE = 3
SEVEN = 7

ALLOWED_NUMBERS = (
        (ZERO, 'Zero'),
        (THREE, 'Three'),
        (SEVEN, 'Seven'),
    )


def test_default_cast_with_flat_list():
    """Default cast with a flat list."""
    choices = Choices(['a', 'b', 'c'])
    assert 'a' == choices('a')
    assert 'b' == choices('b')
    assert 'c' == choices('c')

    with pytest.raises(ValueError):
        choices('d')


def test_cast_to_int_with_flat_list():
    """Cast to int with a flat list."""
    choices = Choices([3, 5, 7], cast=int)
    assert 3 == choices('3')
    assert 5 == choices('5')
    assert 7 == choices('7')

    with pytest.raises(ValueError):
        choices(1)


def test_default_with_django_like_choices():
    """Default cast with a Django-like choices tuple."""
    choices = Choices(choices=ALLOWED_FRUITS)
    assert 'apple' == choices('apple')
    assert 'banana' == choices('banana')
    assert 'coconut' == choices('coconut')

    with pytest.raises(ValueError):
        choices('strawberry')


def test_cast_to_int_with_django_like_choices():
    """Cast to int with a Django-like choices tuple."""
    choices = Choices(cast=int, choices=ALLOWED_NUMBERS)
    assert 0 == choices('0')
    assert 3 == choices('3')
    assert 7 == choices('7')

    with pytest.raises(ValueError):
        choices(1)


def test_default_cast_with_booth_flat_list_and_django_like_choices():
    """Default cast with booth flat list and Django-like choices tuple."""
    choices = Choices(['a', 'b', 'c'], choices=ALLOWED_FRUITS)
    assert 'a' == choices('a')
    assert 'b' == choices('b')
    assert 'c' == choices('c')
    assert 'apple' == choices('apple')
    assert 'banana' == choices('banana')
    assert 'coconut' == choices('coconut')

    with pytest.raises(ValueError):
        choices('d')

    with pytest.raises(ValueError):
        choices('watermelon')


def test_cast_to_int_with_booth_flat_list_and_django_like_choices():
    """Cast to int with booth flat list and Django-like choices tuple."""
    choices = Choices([7, 14, 42], cast=int, choices=ALLOWED_NUMBERS)
    assert 7 == choices('7')
    assert 14 == choices('14')
    assert 42 == choices('42')

    assert 0 == choices('0')
    assert 3 == choices('3')
    assert 7 == choices('7')

    with pytest.raises(ValueError):
        choices('not my fault')

    with pytest.raises(ValueError):
        choices('1')
