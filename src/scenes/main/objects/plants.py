import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import Event, GameObject

PLANTS = {
    0: None,
    1: "Mushroom",
    2: "Sunflower",
}

PLANTS_PRICES = {
    "Mushroom": 50,
    "Sunflower": 50
}

PLANTS_LEVEL_UPS = {
    "Sunflower": {"plant_name": "", "cost": 50000},
    "Mushroom": {"plant_name": "LongMushroom", "cost": 50},
    "LongMushroom": {"plant_name": "BigMushroom", "cost": 50},
    "BigMushroom": {"plant_name": "", "cost": 50000}
}

PLANTS_DESCRIPTIONS = {
    "Sunflower": str(
        "Подсолнышко\n"
        "Класс: дорожное растение\n"
        "Скорость: 5 подсолнышек / 10 сек\n"
        "Следующее улучшение: нет\n"
    ),
    "Mushroom": str(
        "Грибочек\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 0.7 сек\n"
        "Атака: 3 ед / 1 пуля\n"
        "Следующее улучшение: ВысокоГрибка\n"
    ),
    "LongMushroom": str(
        "ВысокоГрибка\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 0.25 сек\n"
        "Атака: 1 ед / 1 пуля\n"
        "Следующее улучшение: Большой гриб\n"
    ),
    "BigMushroom": str(
        "Большой гриб\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 1 сек\n"
        "Атака: 12 ед / 1 пуля\n"
        "Следующее улучшение: Нет\n"
    ),
}

# Базовое растение
class BasePlant(GameObject):
    """Универсальное растение."""
    def __init__(
            self,
            tile_pos: tuple,
            upgrade_description: str = "Ура!"
    ):
        super().__init__()
        self.tile_pos = tile_pos
        self.upgrade_description = upgrade_description

class Mushroom(BasePlant):
    """Небольшой грибок-стрелок"""
    ...

class LongMushroom(BasePlant):
    """Длинный грибок-снайпер"""
    ...

class BigMushroom(BasePlant):
    """Большой гриб"""
    ...

# Подсолнышко.
class Sunflower(BasePlant):
    """Подсолнышко, дающее солнышки."""
    ...


PLANTS_CLASSES = {
    Mushroom: "Mushroom",
    Sunflower: "Sunflower",
    LongMushroom: "LongMushroom",
    BigMushroom: "BigMushroom"
}