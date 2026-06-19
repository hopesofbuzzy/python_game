import logging

from src.config.plants import PLANTS


class InventoryModelComponent:
    """Инвентарь для выбора растений."""
    # Заглушки
    def __init__(self, slots: dict = PLANTS):
        self.active_slot: int = 1
        self.slots = slots
        self.size: int = 10

    def set_active_slot(self, key: str):
        if key.isdigit():
            self.active_slot = int(key)
            logging.debug(f"Слот инвентаря: {self.active_slot}")

    def get_active_slot(self) -> str:
        return self.slots[self.active_slot]

    def get_slots(self):
        return self.slots

    