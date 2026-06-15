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
    Sunflower
)

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
MUSHROOM_COOLDOWN = 0.5
MUSHROOM_PRICE = 50
MUSHROOM_IMAGE_PATH = "res/mushroom.png"
MUSHROOM_RANGE = 2


class PlantBuilder:
    """Строитель растений."""

    def __init__(self, add_object, bullet_factory, give_sun, remove_plant):
        self.add_object = add_object
        self.give_sun = give_sun
        self.bullet_factory = bullet_factory
        self.remove_plant = remove_plant
        self._plant = None
        self.PLANTS = {
            "Mushroom": self.create_mushroom,
            "Sunflower": self.create_sunflower
        }

    def with_plant(self, name: str, *args):
        if name in self.PLANTS:
            plant = self.PLANTS[name](*args)
            plant.tags.add("plant")
            self.add_object(plant)
            self._plant = plant
            return self
        else:
            raise KeyError("Неизвестное растение!")

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
        click_handler.on_button_pressed.subscribe(lambda: logging.debug("Растение нажато"))
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
        sunflower.get(HealthComponent).on_death.subscribe(
            lambda: self.remove_plant(sunflower.tile_pos)
        )
        sunflower.get(HealthComponent).on_death.subscribe(lambda: sunflower.free())
        sunflower.get(CycleTimerComponent).on_timeout.subscribe(self.give_sun)
        return sunflower

    # def with_plant(self, position, tile_pos, cls_model, cls_view):
    #     plant_model = cls_model(local_position=position, tile_pos=tile_pos)
    #     plant = Plant(
    #         model=plant_model,
    #         view=cls_view(self.il),
    #         controller=PlantController(plant_model, cursor)
    #     )
    #     self.add_object(plant)
    #     self._plant = plant
    #     return self

    # def with_button(self):
    #     """Кнопка для взаимодействия с растением."""
    #     if not self._plant:
    #         raise ValueError("Сначала нужно растенеи!")
    #     else:
    #         logging.debug("Рождение кнопки")
    #         button_model = ButtonModel(
    #             local_position=Vector2(0, 0),
    #             parent=self._plant.model
    #         )
    #         button = Button(
    #             model=button_model,
    #             view=View(self.il),
    #             controller=ButtonController(button_model, cursor)
    #         )
    #         if self._plant.controller:
    #             self._plant.controller.attach_button(button.controller)
    #         self.add_object(button)
    #         self._button = button
    #         return self

    # def build(self):
    #     if not self._plant:
    #         raise ValueError("Растение обязательно!")
    #     return self._plant