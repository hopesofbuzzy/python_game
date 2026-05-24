from dataclasses import dataclass, field
from pygame.math import Vector2
import asyncio

from src.core.objects import *
from src.core.systems.event import Event


PLANT_SIZE = Vector2(50, 50)
PLANT_IMAGE_PATH = "res/mushroom.png"

SHOOTER_RANGE = 30
BULLET_SIZE = Vector2(10, 10)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_SPEED = 100

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

@dataclass
class BulletView(SpriteView):
    image_path: str = BULLET_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: BULLET_SIZE)
    ...

@dataclass
class ShooterModel(PlantModel):
    """Растение, стреляющее во врагов на дистанции."""
    range: int = SHOOTER_RANGE
    cooldown = 1.0
    _can_shoot = True
    on_bullet_spawn: Event = field(default_factory=lambda: Event())

    def handle_targets(self, targets: list):
        if self._can_shoot:
            result = self.shoot(targets[0])

    async def shoot(self, target):
        direction = (target.position - self.position).normalize()
        self.on_bullet_spawn.emit(direction, self.position, self)
        self._can_shoot = False
        await asyncio.sleep(self.cooldown)
        self._can_shoot = True

@dataclass
class MushroomModel(ShooterModel):
    """Грибок-стрелок."""
    ...