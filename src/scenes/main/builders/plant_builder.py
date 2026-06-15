import logging
from pygame.math import Vector2

from src.core.systems.event import Event
from src.scenes.main.objects.plants import Bullet, BulletModel, BulletView, Plant, PlantController
from src.core.objects.ui import Button, ButtonController, ButtonModel, ButtonView
from src.core.objects.game_object import View


class PlantBuilder:
    """
        Комплексный строитель растения.

        Инъекции:
            add_object(...),
            image_loader: load_image(...),
            cursor
    """

    def __init__(self, add_object, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        self.add_object = add_object
        self.cursor = cursor
        self._plant: Plant | None = None
        self._button: Button | None = None

    def with_plant(self, position, tile_pos, cls_model, cls_view):
        plant_model = cls_model(local_position=position, tile_pos=tile_pos)
        plant = Plant(
            model=plant_model,
            view=cls_view(self.il),
            controller=PlantController(plant_model, self.cursor)
        )
        self.add_object(plant)
        self._plant = plant
        return self

    def with_button(self):
        """Кнопка для взаимодействия с растением."""
        if not self._plant:
            raise ValueError("Сначала нужно растенеи!")
        else:
            logging.debug("Рождение кнопки")
            button_model = ButtonModel(
                local_position=Vector2(0, 0),
                parent=self._plant.model
            )
            button = Button(
                model=button_model,
                view=View(self.il),
                controller=ButtonController(button_model, self.cursor)
            )
            if self._plant.controller:
                self._plant.controller.attach_button(button.controller)
            self.add_object(button)
            self._button = button
            return self

    def build(self):
        if not self._plant:
            raise ValueError("Растение обязательно!")
        return self._plant