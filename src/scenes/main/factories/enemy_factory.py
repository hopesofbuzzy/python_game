import logging

from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    MovementComponent,
    RectShape,
    PositionComponent,
    PatrolComponent,
    RectComponent,
    UITransform
)

from src.scenes.main.objects import (
    AttackComponent,
    HealthComponent,
    Enemy,
    BarComponent
)

# Enemy
ENEMY_SPEED = 35
ENEMY_HEALTH = 80
ENEMY_SIZE = Vector2(40, 40)
ENEMY_COLOR = (255, 25, 25)

# Общие
ENEMY_ATTACK_COOLDOWN = 0.5
ENEMY_ATTACK = 5

# FastEnemy
FAST_ENEMY_SPEED = 50
FAST_ENEMY_HEALTH = 25
FAST_ENEMY_SIZE = Vector2(30, 30)
FAST_ENEMY_COLOR = (80, 80, 255)

class EnemyFactory:
    """Фабрика сборки врагов."""

    def __init__(self, add_object, ui_factory):
        self.add_object = add_object
        self.ui_factory = ui_factory
        self.ENEMIES = {
            "Enemy": self.create_normal_enemy,
            "FastEnemy": self.create_fast_enemy
        }

    def create_enemy(self, name: str, *args) -> Enemy:
        if name in self.ENEMIES:
            enemy = self.ENEMIES[name](*args)
            enemy.tags.add("enemy")
            self.add_object(enemy)
            # Wiring
            enemy.get(HealthComponent).on_death.subscribe(enemy.free)
            enemy.get(CollisionComponent).on_collision.subscribe(
                enemy.get(AttackComponent).handle_collision
            )
            health_bar = self.ui_factory.create_bar(
                Vector2(0, -30),
                Vector2(50, 10),
                enemy.get(HealthComponent).hp,
                enemy.get(HealthComponent).hp,
                enemy
            )
            enemy.add_child(health_bar)
            enemy.get(HealthComponent).on_damage.subscribe(
                health_bar.get(BarComponent).set_value
            )
            return enemy
        else:
            raise ValueError("Неизвестный враг!")

    def create_normal_enemy(self, position, path):
        position_comp = PositionComponent(position, None)
        movement_comp = MovementComponent(Vector2(0, 0), FAST_ENEMY_SPEED)
        enemy = (
            Enemy()
            .add(position_comp)
            .add(CollisionComponent(RectShape(Vector2(0, 0), ENEMY_SIZE, True), False))
            .add(movement_comp)
            .add(PatrolComponent(position_comp, movement_comp, path))
            .add(RectComponent(ENEMY_COLOR, ENEMY_SIZE, True))
            .add(AttackComponent(movement_comp, "plant", ENEMY_ATTACK, ENEMY_ATTACK_COOLDOWN))
            .add(HealthComponent(ENEMY_HEALTH))
        )
        return enemy

    def create_fast_enemy(self, position, path):
        position_comp = PositionComponent(position, None)
        movement_comp = MovementComponent(Vector2(0, 0), FAST_ENEMY_SPEED)
        enemy = (
            Enemy()
            .add(position_comp)
            .add(CollisionComponent(RectShape(
                    Vector2(0, 0), FAST_ENEMY_SIZE, True
                    ),
                    False
                )
            )
            .add(movement_comp)
            .add(PatrolComponent(position_comp, movement_comp, path))
            .add(RectComponent(FAST_ENEMY_COLOR, FAST_ENEMY_SIZE, True))
            .add(AttackComponent(movement_comp, "plant", ENEMY_ATTACK, ENEMY_ATTACK_COOLDOWN))
            .add(HealthComponent(FAST_ENEMY_HEALTH))
        )
        return enemy