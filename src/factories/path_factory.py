from pygame.math import Vector2

from src.core.objects import PathComponent


class PathFactory:
    """Фабрика сборки выровненного пути для врагов."""

    def create_path_component(self, path, align_method):
        return PathComponent(
            points=list(map(align_method, list(map(Vector2, path)))),
        )
