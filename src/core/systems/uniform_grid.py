from src.core.objects import GameObject, PositionComponent

DEFAULT_CELL_SIZE = 50
DEFAULT_SIZE = 100

class UniformGrid:
    """
    Пространственная структура для эффективных столкновений
    и проверок соседей объектов.
    """

    def __init__(
        self,
        cell_size: int = DEFAULT_CELL_SIZE,
        size: int = DEFAULT_SIZE
    ):
        self.cells: list[list[list]] = []
        self.cell_size = cell_size
        self.size = size
        self.clear()

    def insert(self, object: GameObject):
        """Вставка объекта в нужную клетку GridMap."""
        obj_position = object.get(PositionComponent).position
        cx = int(obj_position.x / self.cell_size)
        cy = int(obj_position.y / self.cell_size)
        self.cells[cy][cx].append(object)

    def query_rect(
        self, object: GameObject, range_x, range_y
    ) -> list[GameObject]:
        """
        Извлечение соседних объектов для целевого объекта.
        range в тайлах.
        """
        obj_position = object.get(PositionComponent).position
        cx = int(obj_position.x / self.cell_size)
        cy = int(obj_position.y / self.cell_size)
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
            < (radius * self.cell_size) ** 2
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
            [list() for _ in range(self.size)] for _ in range(self.size)
        ]

    def in_bounds(self, x, y):
        """Проверка, что координаты на карте."""
        return x in range(0, self.size) and y in range(0, self.size)

    def __repr__(self) -> str:
        """Отображение карты."""
        return f"{self.cells}"
