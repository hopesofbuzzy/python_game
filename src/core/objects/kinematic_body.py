from pygame.math import Vector2
from dataclasses import dataclass, field

from src.core.objects.game_object import Model

@dataclass
class KinematicBodyModel(Model):
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))