import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import (
    AreaModel,
    CircleShape,
    CollisionShape,
    Controller,
    GameObject,
    Model,
    RectShape,
    SpriteView,
    StaticBodyModel,
)
from src.core.objects.ui import (
    Button,
    ButtonModel,
    Dialog,
    DialogModel,
    DialogView
)
from src.core.systems.event import Event
from src.scenes.main.objects.enemy import EnemyModel

# Растения
PLANT_SIZE = Vector2(50, 50)
PLANT_HITBOX_SIZE = Vector2(25, 25)
PLANT_HITBOX_POSITION = PLANT_SIZE // 2
PLANT_IMAGE_PATH = "res/mushroom.png"

# Стрелки
SHOOTER_RANGE = 2
SHOOTER_ATTACK = 3
BULLET_SIZE = Vector2(15, 15)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_SPEED = 150

# Типы растений.
# Подсолнышко
SUNFLOWER_COOLDOWN = 10.0
SUNFLOWER_IMAGE_PATH = "res/sunflower.png"
SUNFLOWER_GIVEN_SUN = 25
SUNFLOWER_PRICE = 50
SUNFLOWER_HEALTH = 25

# Гриб
MUSHROOM_PRICE = 50

# Пуля
BULLET_COOLDOWN = 2.0


# Базовое растение
@dataclass
class PlantModel(AreaModel):
    """Универсальное растение."""
    price: int = 0
    upgrade_description: str = "Ура!"
    tile_pos: tuple = field(default_factory=tuple)


@dataclass
class RoadPlantModel(PlantModel):
    """Растение на дороге (+коллизия)"""
    shape: CollisionShape = field(
        default_factory=lambda: RectShape(
                size=PLANT_HITBOX_SIZE
            )
        )
    health: float = SUNFLOWER_HEALTH

    on_death: Event = field(default_factory=lambda: Event())

    def handle_collision(self, other):
        logging.debug(self.shape)
        if isinstance(other, EnemyModel):
            other.handle_plant_collision(self)

    def damage(self, damage: int):
        logging.debug(f"Урон растению: {damage}")
        self.health -= damage
        if self.health <= 0:
            self.on_death.emit(self.tile_pos)
            self.free()

@dataclass
class PlantView(SpriteView):
    centred: bool = False

@dataclass
class PlantController(Controller):
    on_dialog_requested: Event = field(default_factory=lambda: Event())

    def attach_button(self, button_controller):
        button_controller.on_button_pressed.subscribe(self.on_button_pressed)

    def on_button_pressed(self):
        self.on_dialog_requested.emit(self.model)

@dataclass
class Plant(GameObject[PlantModel, PlantView, PlantController]):
    ...

# Пуля
@dataclass
class BulletModel(AreaModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(
        size=BULLET_SIZE,
        centred=True
    ))
    speed: float = BULLET_SPEED

    _timer: float = BULLET_COOLDOWN
    attack: int = 0

    def handle_collision(self, other):
        """Работает с объектом столкновения."""
        if isinstance(other, EnemyModel):
            other.damage(self.attack)
            self.free()

    def update(self, delta_time):
        self._timer -= delta_time
        if self._timer <= 0.0:
            self.free()


@dataclass
class BulletView(SpriteView):
    image_path: str = BULLET_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: BULLET_SIZE)
    centred: bool = True

@dataclass
class Bullet(GameObject[BulletModel, BulletView, Controller]):
    ...

@dataclass
class ShooterModel(PlantModel):
    """Растение, стреляющее во врагов на дистанции."""

    range: int = SHOOTER_RANGE
    damage: int = SHOOTER_ATTACK
    cooldown: float = 1.0
    _timer: float = 0.0
    on_bullet_spawn: Event = field(default_factory=lambda: Event())

    def handle_targets(self, targets: list, delta_time):
        if self._timer < 0.0:
            self.shoot(targets[0])
        else:
            self._timer -= delta_time

    def shoot(self, target):
        direction = (target.position - self.position - PLANT_SIZE // 2).normalize()
        self.on_bullet_spawn.emit(
            direction, self.position + PLANT_SIZE // 2, self.damage
        )
        self._timer = self.cooldown


# Грибок.
@dataclass
class MushroomModel(ShooterModel):
    """Грибок-стрелок."""
    price: int = MUSHROOM_PRICE


@dataclass
class MushroomView(PlantView):
    image_path: str = PLANT_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: PLANT_SIZE)


# Подсолнышко.
@dataclass
class SunflowerModel(RoadPlantModel):
    """Подсолнышко, дающее солнышки."""
    price: int = SUNFLOWER_PRICE
    cooldown: float = SUNFLOWER_COOLDOWN
    _timer: float = SUNFLOWER_COOLDOWN
    given_sun: int = SUNFLOWER_GIVEN_SUN
    health: float = SUNFLOWER_HEALTH

    on_given_sun: Event = field(default_factory=lambda: Event())

    def update(self, delta_time):
        self._timer -= delta_time
        if self._timer <= 0.0:
            self.on_given_sun.emit(self.given_sun)
            self._timer = self.cooldown


@dataclass
class SunflowerView(PlantView):
    image_path: str = SUNFLOWER_IMAGE_PATH
    size: Vector2 = field(default_factory=lambda: PLANT_SIZE)