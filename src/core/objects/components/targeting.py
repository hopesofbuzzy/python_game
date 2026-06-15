import logging

from pygame.math import Vector2

from src.core.objects.game_object import GameObject
from src.core.objects.components.position import PositionComponent
from src.core.objects.event import Event

DEFAULT_SHOOTER_RANGE = 2
DEFAULT_SHOOTER_ATTACK = 3
DEFAULT_SHOOTER_COOLDOWN = 1.0

class TargetingComponent:
    def __init__(
        self,
        position,
        range: int = DEFAULT_SHOOTER_RANGE,
        damage: int = DEFAULT_SHOOTER_ATTACK,
        cooldown: float = DEFAULT_SHOOTER_COOLDOWN
    ):
        self.position = position
        self.range = range
        self.damage = damage
        self.cooldown = cooldown
        self._timer: float = 0.0
        self.current_target = None
        self.on_shoot: Event = Event()

    def choose_target(self, targets: list[GameObject]):
        if targets:
            self.current_target = targets[0]
        else:
            self.current_target = None

    def update(self, delta_time):
        if self._timer < 0.0:
            if self.current_target:
                target_pos = self.current_target.get(PositionComponent).position
                direction = (target_pos - self.position.position).normalize()
                logging.debug(direction)
                self.on_shoot.emit(
                    direction, self.position.position, self.damage
                )
                self._timer = self.cooldown
        else:
            self._timer -= delta_time