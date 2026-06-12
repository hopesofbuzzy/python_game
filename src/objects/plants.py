from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import AreaModel, CollisionShape, Model, RectShape, SpriteView
from src.core.systems.event import Event
from src.objects import EnemyModel

PLANT_SIZE = Vector2(50, 50)
PLANT_IMAGE_PATH = "res/mushroom.png"

SHOOTER_RANGE = 2
SHOOTER_DAMAGE = 3
BULLET_SIZE = Vector2(15, 15)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_SPEED = 150

# Типы растений.
SUNFLOWER_COOLDOWN = 7
SUNFLOWER_IMAGE_PATH = "res/sunflower.png"


@dataclass
class PlantModel(Model):
    """Универсальное растение."""

    ...

@dataclass
class PlantView(SpriteView): ...

@dataclass
class BulletModel(AreaModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(size=BULLET_SIZE))
    speed: float = BULLET_SPEED
    damage: int = 0

    def handle_collision(self, other):
        """Работает с объектом столкновения."""
        if isinstance(other, EnemyModel):
            other.damage(self.damage)
            self.free()


@dataclass
class BulletView(SpriteView):
    image_path: str = BULLET_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: BULLET_SIZE)


@dataclass
class ShooterModel(PlantModel):
    """Растение, стреляющее во врагов на дистанции."""

    range: int = SHOOTER_RANGE
    damage: int = SHOOTER_DAMAGE
    cooldown: float = 1.0
    _timer: float = 0.0
    on_bullet_spawn: Event = field(default_factory=lambda: Event())

    def handle_targets(self, targets: list, delta_time):
        if self._timer < 0.0:
            self.shoot(targets[0])
        else:
            self._timer -= delta_time

    def shoot(self, target):
        direction = (target.position - self.position).normalize()
        self.on_bullet_spawn.emit(
            direction, self.position + PLANT_SIZE // 2, self.damage
        )
        self._timer = self.cooldown


# Грибок.
@dataclass
class MushroomModel(ShooterModel):
    """Грибок-стрелок."""

    ...


@dataclass
class MushroomView(PlantView):
    image_path: str = PLANT_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: PLANT_SIZE)


# Подсолнышко.
@dataclass
class SunflowerModel(PlantModel): ...


@dataclass
class SunflowerView(PlantView):
    image_path: str = SUNFLOWER_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: PLANT_SIZE)