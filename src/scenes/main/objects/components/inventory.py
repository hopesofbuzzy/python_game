import logging
from dataclasses import dataclass
from functools import singledispatchmethod

from src.config.plants import PLANT_DATA, PLANTS


@dataclass
class Slot:
    name: str
    image_path: str


class InventoryModelComponent:
    """Инвентарь для выбора растений."""

    def __init__(self, raw_slots: dict = PLANTS):
        self.active_slot: int = 0
        self.raw_slots = raw_slots
        self.slots: list[Slot | None] = list()
        self.size: int = 10
        self._set_default_slots()

    # Заглушки
    def _set_default_slots(self):
        """Слоты по умолчанию (инвентарь - постоянный)."""
        for _, name in self.raw_slots.items():
            if name:
                self.slots.append(Slot(name, PLANT_DATA[name]["image_path"]))
            else:
                self.slots.append(None)

    @singledispatchmethod
    def set_active_slot(self, arg):
        """Устанавливает слот инвентаря (перегрузки для Slot, str, int)"""
        raise NotImplementedError("Тип слота не поддерживается!")

    @set_active_slot.register(str)
    def _(self, arg: str):
        if arg.isdigit():
            self.active_slot = int(arg)
            logging.info(f"Слот инвентаря: {self.active_slot}")

    @set_active_slot.register(int)
    def _(self, arg: int):
        self.active_slot = arg
        logging.info(f"Слот инвентаря: {self.active_slot}")

    @set_active_slot.register(Slot)
    def _(self, arg: Slot):
        for idx, slot in enumerate(self.slots):
            if not slot and not arg:
                self.active_slot = 0
            elif slot and slot.name == arg.name:
                self.active_slot = idx
                logging.info(f"Слот инвентаря: {self.active_slot}")

    def set_zero_slot(self):
        """Устаналивает слот без предметов."""
        self.set_active_slot(0)

    def get_active_slot(self) -> Slot | None:
        """Возвращает активный слот."""
        return self.slots[self.active_slot]

    def get_slots(self) -> list[Slot]:
        """Возвращает все слоты инвентаря."""
        return [slot for slot in self.slots if slot]
