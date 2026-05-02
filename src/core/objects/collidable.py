from pygame.math import Vector2
from dataclasses import dataclass, field

from src.core.objects.game_object import Model


# Хитбоксы
@dataclass
class CollisionShape:
    """Форма коллизии."""
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))

@dataclass
class CircleShape(CollisionShape):
    radius: float = 0.0

@dataclass
class RectShape(CollisionShape):
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))


# Объекты с коллизией
@dataclass
class Collidable(Model):
    """Базовая модель объекта с коллизией."""
    shape: CollisionShape = field(
        default_factory=lambda: CircleShape(radius=0)
    )

    def handle_collision(self, other: 'Collidable'):
        """Работает с объектом столкновения."""
        ...

@dataclass
class KinematicBodyModel(Collidable):
    """Модель объекта с кинематикой движения."""
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    speed: float = 100

    def set_velocity(self, dx: float, dy: float):
        self.velocity = Vector2(dx, dy) * self.speed


@dataclass
class StaticBodyModel(Collidable):
    """Модель статичного."""
    ...