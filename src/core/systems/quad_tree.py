from pygame.math import Vector2
import pygame

from src.core.objects import GameObject


class QuadTree:
    """
        Пространственная структура для эффективных столкновений
        и проверок соседей объектов.
    """
    MAX_OBJECTS = 4
    MAX_DEPTH = 6

    def __init__(self, bounds: pygame.Rect):
        self.children: list[QuadTree] = []
        self.depth = 1
        self.bounds = bounds
        self.objects: list[GameObject] = []

    def insert(self, object: GameObject):
        """Вставка объекта в нужный узел QuadTree."""
        if len(self.objects) >= self.MAX_OBJECTS:
            self.subdivide()

        if len(self.children) > 0:
            # Распределение индексов в QuadTree.
            # 0 2
            # 1 3
            idx = 0
            if object.model.position.x > self.bounds.centerx:
                idx = 2
            idx += int(object.model.position.y // self.bounds.centery)
            self.children[idx].insert(object)
        else:
            self.objects.append(object)


    def query(self, area: GameObject):
        ...

    def subdivide(self):
        position = Vector2(self.bounds.topleft)
        size = Vector2(self.bounds.bottomright) - position
        BOUNDS_SIZE = size / 2
        self.children = [
            QuadTree(
                bounds=pygame.Rect(
                    position.x + BOUNDS_SIZE.x * x,
                    position.y + BOUNDS_SIZE.y * y,
                    BOUNDS_SIZE.x,
                    BOUNDS_SIZE.y
                )
            ) for x in range(2) for y in range(2)
        ]
        for object in self.objects:
            # Распределение индексов в QuadTree.
            # 0 2
            # 1 3
            idx = 0
            if object.model.position.x > self.bounds.centerx:
                idx = 2
            idx += int(object.model.position.y // self.bounds.centery)
            self.children[idx].objects.append(object)

    def __repr__(self) -> str:
        return f"{self.bounds}: {[qt.bounds for qt in self.children]}"