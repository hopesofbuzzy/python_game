from pygame.math import Vector2
from dataclasses import dataclass, field

from src.core.objects.game_object import Model

@dataclass
class KinematicBodyModel(Model):
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    speed: float = 100

    def set_velocity(self, dx: float, dy: float):
        self.velocity = Vector2(dx, dy) * self.speed