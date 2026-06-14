import logging
from pygame.math import Vector2

from src.scenes.main.objects.inventory import (
    Inventory,
    InventoryController,
    InventoryModel,
)


class InventoryFactory:
    """Фабрика сборки инвентаря."""

    def __init__(self, add_object, image_loader, cursor):
        # # View инъекция (ImageLoader).
        # self.il = image_loader
        # Controller инъекция.
        self.cursor = cursor
        self.add_object = add_object

    def create_inventory(self):
        model = InventoryModel(local_position=Vector2(0, 0))
        inventory = Inventory(
            model=model, controller=InventoryController(model, self.cursor)
        )
        self.add_object(inventory)
        return inventory
