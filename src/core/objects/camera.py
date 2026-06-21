import logging

from pygame.math import Vector2

from src.core.singletones.event_bus import EventFlow, EventBus
from src.core.systems.input import Cursor

ZOOMES: tuple = (0.8, 1.0, 1.5, 2.0)

class Camera:
    """
    Динамическая камера.
    """

    def __init__(self, cursor: Cursor, event_bus: EventBus, size = Vector2(1200, 700)):
        self.size: Vector2 = size
        event_bus.subscribe("on_mouse_wheel", self.change_zoom)

        self.zoom_idx: int = 2
        self.zoom: float = 1.5
        self.cursor = cursor

        self.position: Vector2 = Vector2(0, 0)

    def change_zoom(self, event: EventFlow, zoom_in: bool):
        """
            Изменение зума камеры.

            Args:
                zoom_in: True = приближение, False = удаление
        """
        zoom_idx = self.zoom_idx
        zoom_idx += 1 if zoom_in else -1
        if zoom_idx >= 0 and zoom_idx < len(ZOOMES):
            self.zoom_idx = zoom_idx
            self.zoom = ZOOMES[self.zoom_idx]

    def get_visible_range(self, tile_size: int, cols: int, rows: int):
        """Вычисление видимых областей для карт тайлов."""
        start_col = max(0, int(self.position.x // tile_size))
        start_row = max(0, int(self.position.y // tile_size))
        end_col = min(
            cols,
            int((self.position.x + self.size.x * (1/self.zoom)) // tile_size) + 2
        )
        end_row = min(
            rows,
            int((self.position.y + self.size.y * (1/self.zoom)) // tile_size) + 2
        )
        return start_col, end_col - 1, start_row, end_row - 1

    def handle_drag(self):
        """Управление перемещением камеры."""
        if self.cursor:
            # Перетаскивание.
            if self.cursor.buttons[2]:
                self.position -= self.cursor.rel_pos
                self.cursor.rel_pos = Vector2(0, 0)

    def to_local(self, position: Vector2):
        """Перевод глобальных координат в экранные."""
        return (position - self.position) * self.zoom

    def to_global(self, position: Vector2):
        """Перевод экранных координат в глобальные."""
        return (position / self.zoom) + self.position
