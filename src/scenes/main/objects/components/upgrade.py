import logging
import sys

from src.core.objects import Event
from src.core.singletones.event_bus import event_bus
from src.scenes.main.objects.plants import PLANTS_LEVEL_UPS

DEFAULT_UPGRADE_SPEED = 25

class UpgradeComponent:
    def __init__(self, plant, target_name: str, target_suns: int):
        self.suns: int = 0
        self.plant = plant
        self.target_name = target_name
        self.target_suns = target_suns

    def request_upgrade_dialog(self):
        event_bus.fire("on_requested_upgrade_dialog", self.plant, self.request_upgrade)

    def request_upgrade(self):
        event_bus.fire(
            "on_requested_upgrade",
            self.plant,
            DEFAULT_UPGRADE_SPEED,
            self.upgrade
        )

    def upgrade(self):
        self.suns += DEFAULT_UPGRADE_SPEED
        logging.debug(f"{sys.getrefcount(self)}")
        logging.debug(f"Сейчас: {self.suns} Цель: {self.target_suns}")
        if self.suns >= self.target_suns:
            event_bus.fire(
                "on_plant_level_uped",
                self.plant,
                self.target_name,
                self.request_upgrade
            )
            self.suns -= 10000

    def get_upgrade_cost(self):
        return DEFAULT_UPGRADE_SPEED