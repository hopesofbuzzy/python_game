import logging

from pygame.math import Vector2

from src.core.objects import Model
from src.core.systems.input import Cursor


class Camera:
    """
    Динамическая камера.
    """
    ZOOMES: tuple = (0.8, 1.0, 1.5, 2.0)

    def __init__(self, cursor, size = Vector2(1200, 700)):
        self.size: Vector2 = size
        self.cursor: Cursor = cursor
        cursor.on_mouse_wheel.subscribe(self.change_zoom)

        self.zoom_idx: int = 2
        self.zoom: float = 1.5

        self.position: Vector2 = Vector2(0, 0)

    def change_zoom(self, up: bool):
        zoom_idx = self.zoom_idx
        zoom_idx += 1 if up else -1
        if zoom_idx >= 0 and zoom_idx < len(self.ZOOMES):
            self.zoom_idx = zoom_idx
            self.zoom = self.ZOOMES[self.zoom_idx]
            logging.debug(f"Zoom+ {self.zoom}")

    def handle_drag(self):
        if self.cursor:
            # Перетаскивание.
            if self.cursor.buttons[2]:
                self.position -= self.cursor.rel_pos
                self.cursor.rel_pos = Vector2(0, 0)

    def to_local(self, position: Vector2):
        return (position - self.position) * self.zoom

    def to_global(self, position: Vector2):
        return (position / self.zoom) + self.position
