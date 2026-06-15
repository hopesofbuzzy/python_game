from typing import Optional, TypeVar

from pygame.math import Vector2


class PositionComponent:
    def __init__(self, local_position: Vector2, parent: Optional["PositionComponent"]):
        self.local_position = local_position.copy()
        self.parent = parent

    @property
    def position(self):
        if self.parent:
            return self.local_position + self.parent.position
        else:
            return self.local_position

    @position.setter
    def position(self, value):
        if self.parent:
            self.local_position = value - self.parent.position
        else:
            self.local_position = value.copy()