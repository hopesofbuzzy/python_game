import logging

from src.core.objects.event import Event


class HealthComponent:
    def __init__(self, hp: int):
        self.hp = hp
        self.on_damage: Event = Event()
        self.on_death: Event = Event()

    def damage(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            logging.debug("Смерть!")
            self.on_death.emit()
        self.on_damage.emit(self.hp)