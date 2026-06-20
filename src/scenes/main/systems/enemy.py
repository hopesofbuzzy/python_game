from src.core.singletones.event_bus import EventBus, EventFlow
from src.scenes.main.objects import Enemy


class EnemyController:
    def __init__(self, event_bus: EventBus):
        event_bus.subscribe("on_enemy_attacked", self.on_enemy_attacked)
        event_bus.subscribe("on_enemy_death", self.remove_enemy)

    def remove_enemy(self, _event: EventFlow, enemy: Enemy):
        enemy.free()

    def on_enemy_attacked(self, _event: EventFlow, enemy: Enemy, target):
        ...