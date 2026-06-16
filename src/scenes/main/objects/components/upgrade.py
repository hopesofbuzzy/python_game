import logging

from src.core.objects import Event
from src.scenes.main.objects.plants import PLANTS_LEVEL_UPS

DEFAULT_UPGRADE_SPEED = 25

class UpgradeComponent:
    def __init__(self, plant, target_name: str, target_suns: int):
        self.suns: int = 0
        self.plant = plant
        self.target_name = target_name
        self.target_suns = target_suns
        self.on_level_up: Event = Event()

    def upgrade(self):
        self.suns += DEFAULT_UPGRADE_SPEED
        logging.debug(f"Сейчас: {self.suns} Цель: {self.target_suns}")
        if self.suns >= self.target_suns:
            logging.debug("LEVEL UP")
            self.on_level_up.emit(self.plant, self.target_name)
            self.suns -= 10000

    def get_upgrade_cost(self):
        return DEFAULT_UPGRADE_SPEED