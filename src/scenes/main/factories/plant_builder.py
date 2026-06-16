import logging

from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    RectShape,
    PositionComponent,
    TargetingComponent,
    SpriteComponent,
    TextRenderComponent,
    ClickHandlerComponent,
    UITransform
)

from src.scenes.main.objects import (
    CycleTimerComponent,
    HealthComponent,
    BasePlant,
    Mushroom,
    Sunflower,
    UpgradeComponent,
    LongMushroom,
    BigMushroom
)

from src.scenes.main.objects import PLANTS_LEVEL_UPS

# from src.core.objects.ui import Button, ButtonController, ButtonModel, ButtonView
# from src.core.objects.game_object import View

# Растения
PLANT_SIZE = Vector2(50, 50)
PLANT_HITBOX_SIZE = Vector2(25, 25)
PLANT_HITBOX_POSITION = PLANT_SIZE // 2
PLANT_IMAGE_PATH = "res/mushroom.png"

# Пули
BULLET_SIZE = Vector2(15, 15)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_SPEED = 150

# Типы растений.
# Подсолнышко
SUNFLOWER_COOLDOWN = 10.0
SUNFLOWER_IMAGE_PATH = "res/sunflower.png"
SUNFLOWER_GIVEN_SUN = 25
SUNFLOWER_PRICE = 50
SUNFLOWER_HEALTH = 15

# Гриб
MUSHROOM_RANGE = 2
MUSHROOM_ATTACK = 3
MUSHROOM_COOLDOWN = 0.7
MUSHROOM_PRICE = 50
MUSHROOM_IMAGE_PATH = "res/mushroom.png"
MUSHROOM_RANGE = 2

# Гриб-снайпер
LONG_MUSHROOM_ATTACK = 1
LONG_MUSHROOM_COOLDOWN = 0.25
LONG_MUSHROOM_IMAGE_PATH = "res/sunflower.png"
LONG_MUSHROOM_RANGE = 4
LONG_MUSHROOM_BULLET_SPEED = 250

BIG_MUSHROOM_ATTACK = 12
BIG_MUSHROOM_COOLDOWN = 1
BIG_MUSHROOM_IMAGE_PATH = "res/mushroom.png"
BIG_MUSHROOM_RANGE = 3
BIG_MUSHROOM_BULLET_SPEED = 200



class PlantBuilder:
    """Строитель растений."""

    def __init__(self, add_object, bullet_factory, give_sun, remove_plant, level_up, upgrade):
        self.add_object = add_object
        self.give_sun = give_sun
        self.bullet_factory = bullet_factory
        self.remove_plant = remove_plant
        self.level_up = level_up
        self.upgrade = upgrade
        self._plant = None
        self.plant_name = ""
        self.PLANTS = {
            "Mushroom": self.create_mushroom,
            "Sunflower": self.create_sunflower,
            "LongMushroom": self.create_long_mushroom,
            "BigMushroom": self.create_big_mushroom
        }

    def with_replace(self, tile_pos: tuple):
        self.remove_plant(tile_pos)
        return self

    def with_plant(self, name: str, *args):
        if name in self.PLANTS:
            plant = self.PLANTS[name](*args)
            self.plant_name = name
            plant.tags.add("plant")
            self.add_object(plant)
            self._plant = plant
            return self
        else:
            raise KeyError("Неизвестное растение!")

    def with_upgrade(self):
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        upgrade = UpgradeComponent(
            self._plant,
            PLANTS_LEVEL_UPS[self.plant_name]["plant_name"],
            PLANTS_LEVEL_UPS[self.plant_name]["cost"]
        )
        self._plant.add(upgrade)
        upgrade.on_level_up.subscribe(self.level_up)
        return self

    def with_button(self):
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        click_handler = ClickHandlerComponent(
            UITransform(
                Vector2(0, 0),
                PLANT_SIZE,
                False,
                anchor=self._plant,
                centred=True
            )
        )
        self._plant.add(click_handler)
        upgrade_func = self.upgrade
        plant = self._plant
        click_handler.on_button_pressed.subscribe(lambda: upgrade_func(plant))
        return self

    def build(self) -> BasePlant:
        if not self._plant:
            raise ValueError("Строителю нужно растение!")
        return self._plant

    def create_mushroom(self, position, tile_pos):
        position_comp = PositionComponent(position, None)
        mushroom = (
            Mushroom(tile_pos, MUSHROOM_PRICE)
            .add(position_comp)
            .add(SpriteComponent(MUSHROOM_IMAGE_PATH, PLANT_SIZE, True))
            .add(TargetingComponent(
                    position_comp,
                    MUSHROOM_RANGE,
                    MUSHROOM_ATTACK,
                    MUSHROOM_COOLDOWN
                )
            )
        )
        logging.debug("Тут ничего не надо!")
        mushroom.get(TargetingComponent).on_shoot.subscribe(
            self.bullet_factory.create_bullet
        )
        return mushroom

    def create_long_mushroom(self, position, tile_pos):
        position_comp = PositionComponent(position, None)
        mushroom = (
            LongMushroom(tile_pos, MUSHROOM_PRICE)
            .add(position_comp)
            .add(SpriteComponent(LONG_MUSHROOM_IMAGE_PATH, PLANT_SIZE, True))
            .add(TargetingComponent(
                    position_comp,
                    LONG_MUSHROOM_RANGE,
                    LONG_MUSHROOM_ATTACK,
                    cooldown=LONG_MUSHROOM_COOLDOWN,
                    speed=LONG_MUSHROOM_BULLET_SPEED
                )
            )
        )
        logging.debug(f"{mushroom.get(TargetingComponent).cooldown}")
        mushroom.get(TargetingComponent).on_shoot.subscribe(
            self.bullet_factory.create_bullet
        )
        return mushroom

    def create_big_mushroom(self, position, tile_pos):
        position_comp = PositionComponent(position, None)
        mushroom = (
            LongMushroom(tile_pos, MUSHROOM_PRICE)
            .add(position_comp)
            .add(SpriteComponent(BIG_MUSHROOM_IMAGE_PATH, PLANT_SIZE, True))
            .add(TargetingComponent(
                    position_comp,
                    BIG_MUSHROOM_RANGE,
                    BIG_MUSHROOM_ATTACK,
                    cooldown=BIG_MUSHROOM_COOLDOWN,
                    speed=BIG_MUSHROOM_BULLET_SPEED
                )
            )
        )
        logging.debug(f"{mushroom.get(TargetingComponent).cooldown}")
        mushroom.get(TargetingComponent).on_shoot.subscribe(
            self.bullet_factory.create_bullet
        )
        return mushroom

    def create_sunflower(self, position, tile_pos):
        sunflower = (
            Sunflower(tile_pos, SUNFLOWER_PRICE)
            .add(PositionComponent(position, None))
            .add(SpriteComponent(SUNFLOWER_IMAGE_PATH, PLANT_SIZE, True))
            .add(CollisionComponent(
                    RectShape(
                        Vector2(0, 0), PLANT_HITBOX_SIZE, True
                    ),
                    False
                )
            )
            .add(CycleTimerComponent(SUNFLOWER_COOLDOWN, SUNFLOWER_GIVEN_SUN))
            .add(HealthComponent(SUNFLOWER_HEALTH))
        )
        remove_plant_func = self.remove_plant
        sunflower.get(HealthComponent).on_death.subscribe(
            lambda: remove_plant_func(sunflower.tile_pos)
        )
        sunflower.get(HealthComponent).on_death.subscribe(lambda: sunflower.free())
        sunflower.get(CycleTimerComponent).on_timeout.subscribe(self.give_sun)
        return sunflower
