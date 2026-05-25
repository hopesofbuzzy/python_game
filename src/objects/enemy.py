import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent
from dataclasses import dataclass, field

from src.core.objects import *

ENEMY_SPEED = 15
ENEMY_HEALTH = 10
ENEMY_SIZE = Vector2(50, 50)
ENEMY_COLOR = (255, 25, 25)

@dataclass
class EnemyModel(PathBodyModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(size=ENEMY_SIZE))
    speed: float = ENEMY_SPEED
    health: int = ENEMY_HEALTH

    def handle_collision(self, other):
        ...

    def damage(self, damage: int):
        print(damage)
        self.health -= damage
        if self.health <= 0:
            self.free()

@dataclass
class EnemyView(RectView):
    color: tuple = ENEMY_COLOR
    size: Vector2 = field(default_factory=lambda: ENEMY_SIZE)