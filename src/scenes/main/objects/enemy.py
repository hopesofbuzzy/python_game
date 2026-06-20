import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects.game_object import GameObject


class Enemy(GameObject):
    def update(self, delta_time):
        return super().update(delta_time)
            