import logging

from pygame.math import Vector2

from src.core.objects.game_object import GameObject
from src.core.objects.components.position import PositionComponent
from src.core.objects.event import Event

DEFAULT_SHOOTER_RANGE = 2
DEFAULT_SHOOTER_ATTACK = 3
DEFAULT_SHOOTER_COOLDOWN = 3.0
DEFAULT_SHOOTER_BULLET_SPEED = 150

class TargetingComponent:
    def __init__(
        self,
        position,
        range: int = DEFAULT_SHOOTER_RANGE,
        damage: int = DEFAULT_SHOOTER_ATTACK,
        cooldown: float = DEFAULT_SHOOTER_COOLDOWN,
        speed: float = DEFAULT_SHOOTER_BULLET_SPEED
    ):
        self.position = position
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self.speed = speed
        self._timer: float = 0.0
        self.queue = list()
        self.on_shoot: Event = Event()

    def choose_target(self, targets: list[GameObject]):
        if targets:
            for target in targets:
                if target not in self.queue:
                    self.queue.append(target)
            if self.queue[0] not in targets:
                self.queue.pop(0)
        else:
            self.queue = list()

    def update(self, delta_time):
        if self._timer < 0.0:
            if self.queue:
                target_pos = self.queue[0].get(PositionComponent).position
                direction = (target_pos - self.position.position).normalize()
                self.on_shoot.emit(
                    direction, self.position.position, self.damage, self.speed
                )
                
                self._timer = self.cooldown
        else:
            self._timer -= delta_time