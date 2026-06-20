import logging

from pygame.math import Vector2

from src.scenes.main.objects import (
    Inventory,
    InventoryModelComponent,
    KeyControllerComponent,
)


class InventoryFactory:
    """Фабрика сборки инвентаря."""

    def __init__(self, add_object):
        self.add_object = add_object

    def create_inventory(self):
        key_controller = KeyControllerComponent()
        inventory_model = InventoryModelComponent()
        inventory = (
            Inventory()
            .add(inventory_model)
            .add(key_controller)
        )
        key_controller.on_key_pressed.subscribe(inventory_model.set_active_slot)
        self.add_object(inventory)
        return inventory