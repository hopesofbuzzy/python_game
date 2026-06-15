import logging

from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    RectShape,
    PositionComponent,
    TargetingComponent,
    SpriteComponent
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
SUNFLOWER_HEALTH = 25

# Гриб
MUSHROOM_RANGE = 2
MUSHROOM_ATTACK = 3
MUSHROOM_COOLDOWN = 0.5
MUSHROOM_PRICE = 50
MUSHROOM_IMAGE_PATH = "res/mushroom.png"
MUSHROOM_RANGE = 2


class PlantFactory:
    """Фабрика растений."""

    def __init__(self, add_object):
        self.add_object = add_object
        self.PLANTS = {
            "Mushroom": self.create_mushroom,
            "Sunflower": self.create_sunflower
        }

    def create_plant(self, name: str, *args) -> BasePlant:
        if name in self.PLANTS:
            plant = self.PLANTS[name](*args)
            plant.tags.add("plant")
            self.add_object(plant)
            return plant
        else:
            raise KeyError("Неизвестное растение!")

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
        sunflower.get(HealthComponent).on_death.subscribe(sunflower.free)
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