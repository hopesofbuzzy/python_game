import logging
from dataclasses import dataclass

from src.config.plants import (
    PLANTS,
    PLANT_DATA
)

@dataclass
class Slot:
    name: str
    image_path: str


class InventoryModelComponent:
    """Инвентарь для выбора растений."""
    # Заглушки
    def __init__(self, raw_slots: dict = PLANTS):
        self.active_slot: int = 1
        self.raw_slots = raw_slots
        self.slots: list[Slot] = list()
        self.size: int = 10
        self._set_default_slots()

    def _set_default_slots(self):
        for idx, name in self.raw_slots.items():
            if name:
                self.slots.append(Slot(name, PLANT_DATA[name]["image_path"]))
            else:
                self.slots.append(Slot("None", "None"))

    def set_active_slot(self, key: str):
        if key.isdigit():
            self.active_slot = int(key)
            logging.debug(f"Слот инвентаря: {self.active_slot}")

    def get_active_slot(self) -> Slot:
        return self.slots[self.active_slot]

    def get_slots(self) -> list[Slot]:
        return self.slots

    