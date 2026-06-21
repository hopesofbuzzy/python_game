from pygame.math import Vector2

from src.core.singletones.event_bus import EventBus, EventFlow
from src.factories.enemy_factory import EnemyFactory
from src.scenes.main.objects import Enemy


class EnemyController:
    """Контроллер спавна врагов."""

    def __init__(self, enemy_factory: EnemyFactory, event_bus: EventBus):
        self.enemies = list()
        self.enemies_destroyed = 0
        self.enemy_factory = enemy_factory
        event_bus.subscribe("on_enemy_attacked", self.on_enemy_attacked)
        event_bus.subscribe("on_enemy_death", self.remove_enemy)
        event_bus.subscribe("on_enemy_spawn", self.spawn_enemy)
        self.event_bus = event_bus

    def spawn_enemy(self, _event: EventFlow, enemy: str, path):
        """Спавнит сущность enemy с путём path."""
        self.enemies.append(
            self.enemy_factory.create_enemy(enemy, Vector2(0, 00), path)
        )

    def remove_enemy(self, _event: EventFlow, enemy: Enemy):
        """Уничтожает сущность enemy."""
        enemy.free()
        self.enemies.remove(enemy)
        self.event_bus.fire("on_enemy_deleted", len(self.enemies))
        self.enemies_destroyed += 1

    def on_enemy_attacked(self, _event: EventFlow, enemy: Enemy, target): ...

    def get_enemies_destroyed_count(self):
        """Возвращает статистику уничтоженных врагов."""
        return self.enemies_destroyed
