import logging

from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    MovementComponent,
    PositionComponent,
    RectComponent,
    RectShape,
)
from src.scenes.main.objects import AttackComponent, Bullet, TimerComponent

BULLET_SIZE = Vector2(15, 15)
BULLET_IMAGE_PATH = "res/mushroom.png"
BULLET_COLOR = (255, 255, 255)
BULLET_SPEED = 150
BULLET_COOLDOWN = 1.5

class BulletFactory:
    """Фабрика сборки пули растения."""

    def __init__(self, add_object):
        self.add_object = add_object

    def create_bullet(self, direction, position, attack, speed):
        logging.debug("Пуля создана!")
        collision = CollisionComponent(
            RectShape(Vector2(0, 0), BULLET_SIZE, True),
            False
        )
        timer_remove = TimerComponent(BULLET_COOLDOWN)
        movement = MovementComponent(direction * speed, speed)
        attack_component = AttackComponent(movement, "enemy", attack, BULLET_COOLDOWN)
        bullet = (
            Bullet()
            .add(PositionComponent(position, None))
            .add(collision)
            .add(movement)
            .add(timer_remove)
            .add(attack_component)
            .add(RectComponent(BULLET_COLOR, BULLET_SIZE, centred=True))
        )
        timer_remove.on_timeout.subscribe(bullet.free)
        collision.on_collision.subscribe(attack_component.handle_collision)
        attack_component.on_attack.subscribe(bullet.free)
        self.add_object(bullet)
        return bullet