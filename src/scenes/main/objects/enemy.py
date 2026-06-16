import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import GameObject, MovementComponent
from src.scenes.main.objects.components.attack import AttackComponent


class Enemy(GameObject):
    def update(self, delta_time):
        return super().update(delta_time)
            