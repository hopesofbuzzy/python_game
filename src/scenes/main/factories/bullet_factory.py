import logging
from dataclasses import dataclass
from typing import Callable

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

@dataclass
class BuildContext:
    attack_func: Callable
    timeout_func: Callable

class BulletFactory:
    """Фабрика сборки пули растения."""

    def __init__(self, add_object, event_bus):
        self.add_object = add_object
        self.build_context = BuildContext(
            attack_func=lambda bullet, target: event_bus.fire("on_bullet_attacked", bullet, target),
            timeout_func=lambda bullet: event_bus.fire("on_bullet_timeout", bullet)
        )

    def create_bullet(
        self,
        direction: Vector2,
        position: Vector2,
        attack: int,
        speed: int
    ):
        """
            Создаёт пулю.

            Args:
                direction: направление пули.
                position: позиция пули.
                attack: урон.
                speed: скорость пули.
        """
        logging.debug("Пуля создана!")
        bullet = Bullet()
        collision = CollisionComponent(
            bullet,
            RectShape(Vector2(0, 0), BULLET_SIZE, True),
            False
        )
        timer_remove = TimerComponent(bullet, BULLET_COOLDOWN, bullet)
        movement = MovementComponent(direction * speed, speed)
        attack_component = AttackComponent(bullet, "enemy", attack, BULLET_COOLDOWN)
        bullet = (
            bullet
            .add(PositionComponent(position, None))
            .add(collision)
            .add(movement)
            .add(timer_remove)
            .add(attack_component)
            .add(RectComponent(BULLET_COLOR, BULLET_SIZE, centred=True))
        )
        timer_remove.bind(self.build_context)
        attack_component.bind(self.build_context)
        self.add_object(bullet)
        return bullet