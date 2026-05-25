from dataclasses import dataclass, field
from pygame.math import Vector2
import asyncio

from src.core.objects import *
from src.objects import EnemyModel
from src.core.systems.event import Event


PLANT_SIZE = Vector2(50, 50)
PLANT_IMAGE_PATH = "res/mushroom.png"

SHOOTER_RANGE = 2
BULLET_SIZE = Vector2(15, 15)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_SPEED = 150

@dataclass
class PlantModel(Model):
    """Универсальное растение."""
    ...

@dataclass
class PlantView(SpriteView):
    image_path: str = PLANT_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: PLANT_SIZE)

@dataclass
class BulletModel(AreaModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(size=BULLET_SIZE))
    speed: float = BULLET_SPEED

    def handle_collision(self, other):
        """Работает с объектом столкновения."""
        if isinstance(other, EnemyModel):
            self.free()

@dataclass
class BulletView(SpriteView):
    image_path: str = BULLET_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: BULLET_SIZE)

@dataclass
class ShooterModel(PlantModel):
    """Растение, стреляющее во врагов на дистанции."""
    range: int = SHOOTER_RANGE
    cooldown = 1.0
    _timer: float = 0.0
    on_bullet_spawn: Event = field(default_factory=lambda: Event())

    def handle_targets(self, targets: list, delta_time):
        if self._timer < 0.0:
            self.shoot(targets[0])
        else:
            self._timer -= delta_time

    def shoot(self, target):
        direction = (target.position - self.position).normalize()
        self.on_bullet_spawn.emit(direction, self.position + PLANT_SIZE // 2, self)
        self._timer = self.cooldown

@dataclass
class MushroomModel(ShooterModel):
    """Грибок-стрелок."""
    ...