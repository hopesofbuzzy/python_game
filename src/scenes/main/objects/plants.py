import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import (
    GameObject,
    Event
)

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

# Базовое растение
class BasePlant(GameObject):
    """Универсальное растение."""
    def __init__(
            self,
            tile_pos: tuple,
            price: int = 0,
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