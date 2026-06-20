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
    death_func: Callable

class EnemyFactory:
    """Фабрика сборки врагов."""

    def __init__(self, add_object, damage_func, remove_func, ui_factory):
        self.add_object = add_object
        self.build_context = BuildContext(
            damage_func=damage_func,
            death_func=remove_func
        )
        self.ui_factory = ui_factory

    def create_enemy(self, name: str, position: Vector2, path) -> Enemy:
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
            
            enemy.tags.add("enemy")
            self.add_object(enemy)
            # Проводка
            health_comp = enemy.get(HealthComponent)
            health_comp.bind(self.build_context)
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
            return enemy
        else:
            raise ValueError("Неизвестный враг!")