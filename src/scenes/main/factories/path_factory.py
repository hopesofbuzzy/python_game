import logging
from pygame.math import Vector2

from src.core.objects.path import (
    PathModel,
)

class PathFactory:
    """Фабрика сборки выровненного пути для врагов."""
    def create_path(self, path, align_method):
        return PathModel(
            local_position=Vector2(0, 0),
            points=list(
                map(
                    align_method,
                    list(map(Vector2, path))
                )
            ),
        )
