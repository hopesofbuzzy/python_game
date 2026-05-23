from pygame.math import Vector2
from dataclasses import dataclass, field
from src.core.objects import Model


@dataclass
class Camera:
    size: Vector2 = field(default_factory=lambda: Vector2(1200, 700))

    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    target: Model | None = None
    def follow(self):
        if self.target:
            self.position = self.target.position - self.size // 2

    def to_local(self, position: Vector2):
        return position - self.position