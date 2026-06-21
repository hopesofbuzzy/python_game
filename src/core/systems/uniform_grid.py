from src.core.objects import GameObject, PositionComponent


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
        obj_position = object.get(PositionComponent).position
        cx = int(obj_position.x / self.CELL_SIZE)
        cy = int(obj_position.y / self.CELL_SIZE)
        self.cells[cy][cx].append(object)

    def query_rect(
        self, object: GameObject, range_x, range_y
    ) -> list[GameObject]:
        """
        Извлечение соседних объектов для целевого объекта.
        range в тайлах.
        """
        obj_position = object.get(PositionComponent).position
        cx = int(obj_position.x / self.CELL_SIZE)
        cy = int(obj_position.y / self.CELL_SIZE)
        result = list()
        for dy in range(-range_x, range_x + 1):
            for dx in range(-range_y, range_y + 1):
                if self.in_bounds(cy + dy, cx + dx):
                    result += self.cells[cy + dy][cx + dx]
        return result

    def query_circle(self, object: GameObject, radius) -> list[GameObject]:
        """
        Извлечение соседних объектов для целевого объекта.
        radius в тайлах.
        """
        candidates = self.query_rect(object, radius, radius)
        center = object.get(PositionComponent).position
        return [
            cndt
            for cndt in candidates
            if (center - cndt.get(PositionComponent).position).length_squared()
            < (radius * self.CELL_SIZE) ** 2
        ]

    def update(self, scene):
        """Очистка и пересоздание UniformGrid."""
        self.clear()
        for object in scene.object_registry.values():
            if object.has(PositionComponent):
                self.insert(object)

    def clear(self):
        """Очистка карты.."""
        self.cells: list[list[list]] = [
            [list() for _ in range(self.SIZE)] for _ in range(self.SIZE)
        ]

    def in_bounds(self, x, y):
        """Проверка, что координаты на карте."""
        return x in range(0, self.SIZE) and y in range(0, self.SIZE)

    def __repr__(self) -> str:
        """Отображение карты."""
        return f"{self.cells}"
