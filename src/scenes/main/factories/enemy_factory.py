import logging
from dataclasses import dataclass
from typing import Callable

from pygame.math import Vector2

from src.config.enemies import ENEMY_DATA
from src.core.objects import (
    CollisionComponent,
    MovementComponent,
    PatrolComponent,
    PositionComponent,
    RectComponent,
    RectShape,
)
from src.scenes.main.objects import (
    AttackComponent,
    BarComponent,
    Enemy,
    HealthComponent,
)


@dataclass
class BuildContext:
    damage_func: Callable
    attack_func: Callable
    death_func: Callable
    end_patrol_func: Callable

class EnemyFactory:
    """Фабрика сборки врагов."""

    def __init__(self, add_object, ui_factory, event_bus):
        self.add_object = add_object
        self.build_context = BuildContext(
            attack_func=lambda enemy, target: event_bus.fire("on_enemy_attacked", enemy, target),
            damage_func=lambda enemy: event_bus.fire("on_enemy_damaged", enemy),
            death_func=lambda enemy: event_bus.fire("on_enemy_death", enemy),
            end_patrol_func=lambda: event_bus.fire("on_enemy_reached_end")
        )
        self.ui_factory = ui_factory

    def create_enemy(self, name: str, position: Vector2, path) -> Enemy:
        """
            Создаёт врага.

            Args:
                name: название врага.
                position: позиция появления.
                path: путь патрулирования (список координат).
        """
        if name in ENEMY_DATA:
            # Инициализация врага
            enemy = Enemy()
            # Харакеристики
            speed = ENEMY_DATA[name]["speed"]
            size = ENEMY_DATA[name]["size"]
            color = ENEMY_DATA[name]["color"]
            attack = ENEMY_DATA[name]["attack"]
            attack_cooldown = ENEMY_DATA[name]["attack_cooldown"]
            health = ENEMY_DATA[name]["health"]
            # Компоненты
            enemy.add(PositionComponent(position, None))
            enemy.add(CollisionComponent(
                enemy,
                RectShape(
                    Vector2(0, 0),
                    size,
                    True
                ), 
                False
            ))
            enemy.add(MovementComponent(Vector2(0, 0), speed))
            enemy.add(PatrolComponent(enemy, path))
            enemy.add(RectComponent(color, size, True))
            enemy.add(AttackComponent(
                enemy,
                "plant",
                attack,
                attack_cooldown
            ))
            enemy.add(HealthComponent(enemy, health))
            # Bind
            enemy.get(AttackComponent).bind(self.build_context)
            enemy.get(PatrolComponent).bind(self.build_context)
            enemy.tags.add("enemy")
            self.add_object(enemy)
            self._add_healthbar(enemy)
            return enemy
        else:
            raise ValueError("Неизвестный враг!")

    def _add_healthbar(self, enemy):
        """Добавляет врагу шкалу здоровья."""
        health_comp = enemy.get(HealthComponent)
        health_comp.bind(self.build_context)
        # Шкала здоровья.
        health_bar = self.ui_factory.create_bar(
            Vector2(0, -30),
            Vector2(50, 10),
            health_comp.hp,
            health_comp.hp,
            enemy
        )
        enemy.add_child(health_bar)
        health_comp.damage_func = (
            health_bar.get(BarComponent).set_value
        )