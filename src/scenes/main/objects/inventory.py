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
    1: Slot(MushroomModel, MushroomView),
    2: Slot(SunflowerModel, SunflowerView),
}


@dataclass
class InventoryModel(Model):
    """Инвентарь для выбора растений."""
    # Заглушки
    active_slot: int = 1
    size: int = 10

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
                    self.model.active_slot = int(event.dict["unicode"])
                    logging.debug(f"Слот инвентаря: {self.model.active_slot}")

@dataclass
class Inventory(GameObject[InventoryModel, InventoryView, InventoryController]):
    ...