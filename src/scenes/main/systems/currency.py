import logging

from src.config.plants import PLANTS_PRICES
from src.core.objects.event import Event
from src.core.singletones.event_bus import EventBus, EventFlow

DEFAULT_SUNS = 235


class CurrencyManager:
    def __init__(self, event_bus: EventBus, suns: int = DEFAULT_SUNS):
        self.suns: int = suns
        self.on_suns_update: Event = Event()
        event_bus.subscribe("on_given_sun", self.give_sun)

    def give_sun(self, _event: EventFlow, suns: int):
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

    def get_suns(self):
        return self.suns
