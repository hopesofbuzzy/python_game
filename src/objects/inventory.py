import logging
from dataclasses import dataclass, field

import pygame

from src.core.objects import Controller, Model, View
from src.objects.plants import (
    MushroomModel,
    MushroomView,
    SunflowerModel,
    SunflowerView,
)


class Slot:
    """Слот инвентаря с растением для посадки."""

    def __init__(self, model, view):
        self.model = model
        self.view = view


@dataclass
class InventoryModel(Model):
    """Инвентарь для выбора растений."""
    # Заглушки
    slots: dict = field(
        default_factory=lambda: {
            1: Slot(MushroomModel, MushroomView),
            2: Slot(SunflowerModel, SunflowerView),
        }
    )
    active_slot: int = 1
    size: int = 10


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
