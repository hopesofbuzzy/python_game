import logging

from src.core.objects.components.component_registry import ComponentRegistry
from src.core.objects.event import Event


@ComponentRegistry.register("health")
class HealthComponent:
    """Компонент здоровья."""

    def __init__(self, entity, hp: int):
        self.hp = hp
        self.entity = entity
        self.on_damage: Event = Event()

    def bind(self, build_context):
        self.death_func = build_context.death_func
        self.damage_func = build_context.damage_func

    def damage(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            logging.debug("Смерть!")
            self.death_func(self.entity)
        self.damage_func(self.hp)
