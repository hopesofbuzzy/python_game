import logging
from dataclasses import dataclass, field

import pygame

from src.core.objects import Controller, GameObject, Model, View
from src.scenes.main.objects.plants import (
    MushroomModel,
    MushroomView,
    PlantModel,
    PlantView,
    SunflowerModel,
    SunflowerView,
)


class Slot:
    """Слот инвентаря с растением для посадки."""
    def __init__(self, model, view):
        self.model: PlantModel = model
        self.view: PlantView = view

PLANTS = {
    0: None,
    1: Slot(MushroomModel, MushroomView),
    2: Slot(SunflowerModel, SunflowerView),
}


@dataclass
class InventoryModel(Model):
    """Инвентарь для выбора растений."""
    # Заглушки
    active_slot: int = 1
    size: int = 10

    def set_active_slot(self, key: str):
        if key.isdigit():
            self.active_slot = int(key)
            logging.debug(f"Слот инвентаря: {self.active_slot}")

    def get_active_slot(self):
        return PLANTS[self.active_slot]


@dataclass
class InventoryView(View): ...


@dataclass
class InventoryController(Controller):
    def handle_input(self, event):
        match event.type:
            case pygame.KEYDOWN:
                if event.dict["unicode"].isdigit():
                    self.model.set_active_slot(event.dict["unicode"])

@dataclass
class Inventory(GameObject[InventoryModel, InventoryView, InventoryController]):
    ...