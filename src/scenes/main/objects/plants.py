import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import Event, GameObject

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
