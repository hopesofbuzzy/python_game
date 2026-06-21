from typing import Callable

from pygame.math import Vector2

from src.core.objects import GameObject, PositionComponent
from src.scenes.main.objects import CursorCircleComponent


class CursorCircleFactory:
    """Фабрика окружности для привязки к курсору."""

    def __init__(self, add_object: Callable):
        self.add_object = add_object

    def create_cursor_circle(self, radius: int, color: tuple):
        cursor_circle = GameObject()
        cursor_circle.add(PositionComponent(Vector2(0, 0), None))
        cursor_circle.add(CursorCircleComponent(cursor_circle, radius, color))
        cursor_circle.z_index = 50
        self.add_object(cursor_circle)
        return cursor_circle