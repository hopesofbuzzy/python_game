import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import (
    CollisionShape,
    Controller,
    GameObject,
    PathBodyModel,
    RectShape,
    RectView,
)
from src.core.systems.event import Event

# Enemy
ENEMY_SPEED = 35
ENEMY_HEALTH = 50
ENEMY_SIZE = Vector2(40, 40)
ENEMY_COLOR = (255, 25, 25)
ENEMY_ATTACK_COOLDOWN = 0.5
ENEMY_ATTACK = 5

# FastEnemy
FAST_ENEMY_SPEED = 50
FAST_ENEMY_HEALTH = 25
FAST_ENEMY_SIZE = Vector2(30, 30)
FAST_ENEMY_COLOR = (80, 80, 255)


@dataclass
class EnemyModel(PathBodyModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(
        size=ENEMY_SIZE,
        centred=True
        )
    )
    speed: float = field(default_factory=lambda: ENEMY_SPEED)
    health: int = ENEMY_HEALTH
    _attack_timer: float = 0.0
    attack: float = ENEMY_ATTACK

    def handle_collision(self, other):
        ...

    def handle_plant_collision(self, plant):
        if self._attack_timer <= 0.0:
            plant.damage(self.attack)
            self.set_velocity(0, 0)
            self._attack_timer = ENEMY_ATTACK_COOLDOWN
        
    def update(self, delta_time):
        if self._attack_timer >= 0.0:
            self._attack_timer -= delta_time
        else:
            return super().update(delta_time)

    def damage(self, damage: int):
        logging.debug(f"Урон врагу: {damage}")
        self.health -= damage
        if self.health <= 0:
            self.free()


@dataclass
class EnemyView(RectView):
    color: tuple = ENEMY_COLOR
    size: Vector2 = field(default_factory=lambda: ENEMY_SIZE)
    centred: bool = True


@dataclass
class FastEnemyModel(EnemyModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(
        size=FAST_ENEMY_SIZE,
        centred=True
        )
    )
    speed: float = FAST_ENEMY_SPEED
    health: int = FAST_ENEMY_HEALTH


@dataclass
class FastEnemyView(EnemyView):
    color: tuple = FAST_ENEMY_COLOR
    size: Vector2 = field(default_factory=lambda: FAST_ENEMY_SIZE)


@dataclass
class Enemy(GameObject[EnemyModel, EnemyView, Controller]):
    ...