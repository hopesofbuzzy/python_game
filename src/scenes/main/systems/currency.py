import logging

from src.core.objects.event import Event
from src.scenes.main.objects.plants import PLANTS_PRICES

DEFAULT_SUNS = 400

class CurrencyManager:
    def __init__(self, suns: int = DEFAULT_SUNS):
        self.suns: int = suns
        self.on_suns_update: Event = Event()

    def give_sun(self, suns: int):
        """Выдача солыншек."""
        self.suns += suns
        self.on_suns_update.emit(self.suns)

    def decrease_suns(self, suns: int):
        self.suns -= suns
        self.on_suns_update.emit(self.suns)

    def check_suns(self, plant: str) -> bool:
        return self.suns >= PLANTS_PRICES[plant]

    def get_plant_price(self, plant: str) -> int:
        return PLANTS_PRICES[plant]

    def print_current_suns(self):
        logging.debug(f"Текущие солнышки: {self.suns}")