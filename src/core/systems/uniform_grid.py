from pygame.math import Vector2
import pygame

from src.core.objects import GameObject


class UniformGrid:
    """
        Пространственная структура для эффективных столкновений
        и проверок соседей объектов.
    """
    CELL_SIZE = 50
    SIZE = 100

    def __init__(self):
        self.cells: list[list[list]] = []
        self.clear()

    def insert(self, object: GameObject):
        """Вставка объекта в нужную клетку GridMap."""
        cx = int(object.model.position.x / self.CELL_SIZE)
        cy = int(object.model.position.x / self.CELL_SIZE)
        self.cells[cy][cx].append(object)

    def query(self, object: GameObject) -> list[GameObject]:
        """Извлечение соседних объектов для целевого объекта."""
        cx = int(object.model.position.x / self.CELL_SIZE)
        cy = int(object.model.position.x / self.CELL_SIZE)
        result = list()
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if self.in_bounds(cy + dy, cx + dx):
                    result += self.cells[cy + dy][cx + dx]
        return result

    def clear(self):
        self.cells: list[list[list]] = [
            [list() for _ in range(self.SIZE)] for _ in range(self.SIZE)
        ]

    def in_bounds(self, x, y):
        """Проверка, что координаты на карте."""
        return x in range(0, self.SIZE) and y in range(0, self.SIZE)

    def __repr__(self) -> str:
        return f"{self.cells}"