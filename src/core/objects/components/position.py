from typing import Optional, TypeVar

from pygame.math import Vector2

from src.core.objects.game_object import GameObject


class PositionComponent:
    """Компонент позиции с вычислением относительно родительской позиции."""
    def __init__(self, local_position: Vector2, parent: Optional["GameObject"]):
        self.local_position = local_position.copy()
        self.parent = parent

    @property
    def position(self) -> Vector2:
        """Позиция с учётом позиции родителя."""
        if self.parent:
            return self.local_position + self.parent.get(PositionComponent).position
        else:
            return self.local_position

    @position.setter
    def position(self, value):
        if self.parent:
            self.local_position = value - self.parent.get(PositionComponent).position
        else:
            self.local_position = value.copy()