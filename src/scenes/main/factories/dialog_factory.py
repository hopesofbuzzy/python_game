import logging

from pygame.math import Vector2

from src.core.objects.game_object import View
from src.core.objects.components.ui import (
    Button,
    ButtonController,
    ButtonModel,
    ButtonView,
    Dialog,
    DialogModel,
    DialogView,
)
from src.scenes.main.objects.plants import Bullet, BulletModel, BulletView, Plant


class DialogFactory:
    """
        Фабрика сборки объектов сцены

        Инъекции:
            add_object(...),
            image_loader: load_image(...),
            cursor: ...
    """

    def __init__(self, add_object, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        # Controller инъекция.
        cursor = cursor
        self.add_object = add_object

    def create_dialog(self, plant_model):
        ...
