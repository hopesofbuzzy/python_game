import logging

from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    MovementComponent,
    PatrolComponent,
    PositionComponent,
    RectComponent,
    RectShape,
    UITransform,
)
from src.scenes.main.objects import (
    AttackComponent,
    BarComponent,
    Enemy,
    HealthComponent,
)
from src.config.enemies import ENEMY_DATA

class EnemyFactory:
    """Фабрика сборки врагов."""

    def __init__(self, add_object, ui_factory):
        self.add_object = add_object
        self.ui_factory = ui_factory

    def create_enemy(self, name: str, position: Vector2, path) -> Enemy:
        if name in ENEMY_DATA:
            # Харакеристики
            speed = ENEMY_DATA[name]["speed"]
            size = ENEMY_DATA[name]["size"]
            color = ENEMY_DATA[name]["color"]
            attack = ENEMY_DATA[name]["attack"]
            attack_cooldown = ENEMY_DATA[name]["attack_cooldown"]
            health = ENEMY_DATA[name]["health"]
            # Комопненты
            position_comp = PositionComponent(position, None)
            collision_comp = CollisionComponent(
                RectShape(
                    Vector2(0, 0),
                    size,
                    True
                ), 
                False
            )
            movement_comp = MovementComponent(Vector2(0, 0), speed)
            health_comp = HealthComponent(health)
            attack_comp = AttackComponent(
                movement_comp,
                "plant",
                attack,
                attack_cooldown
            )
            # Инициализация врага
            enemy = (
                Enemy()
                .add(position_comp)
                .add(collision_comp)
                .add(movement_comp)
                .add(PatrolComponent(position_comp, movement_comp, path))
                .add(RectComponent(color, size, True))
                .add(attack_comp)
                .add(health_comp)
            )
            enemy.tags.add("enemy")
            self.add_object(enemy)
            # Проводка
            health_comp.on_death.subscribe(enemy.free)
            collision_comp.on_collision.subscribe(
                attack_comp.handle_collision
            )
            health_bar = self.ui_factory.create_bar(
                Vector2(0, -30),
                Vector2(50, 10),
                health_comp.hp,
                health_comp.hp,
                enemy
            )
            enemy.add_child(health_bar)
            health_comp.on_damage.subscribe(
                health_bar.get(BarComponent).set_value
            )
            return enemy
        else:
            raise ValueError("Неизвестный враг!")