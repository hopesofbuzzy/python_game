import logging

from pygame.math import Vector2

from src.core.singletones.event_bus import EventFlow, event_bus
from src.core.systems.input import cursor


class Camera:
    """
    Динамическая камера.
    """
    ZOOMES: tuple = (0.8, 1.0, 1.5, 2.0)

    def __init__(self, size = Vector2(1200, 700)):
        self.size: Vector2 = size
        event_bus.subscribe("on_mouse_wheel", self.change_zoom)

        self.zoom_idx: int = 2
        self.zoom: float = 1.5

        self.position: Vector2 = Vector2(0, 0)

    def change_zoom(self, event: EventFlow, up: bool):
        zoom_idx = self.zoom_idx
        zoom_idx += 1 if up else -1
        if zoom_idx >= 0 and zoom_idx < len(self.ZOOMES):
            self.zoom_idx = zoom_idx
            self.zoom = self.ZOOMES[self.zoom_idx]
            # logging.debug(f"Zoom+ {self.zoom}")

    def handle_drag(self):
        if cursor:
            # Перетаскивание.
            if cursor.buttons[2]:
                self.position -= cursor.rel_pos
                cursor.rel_pos = Vector2(0, 0)

    def to_local(self, position: Vector2):
        return (position - self.position) * self.zoom

    def to_global(self, position: Vector2):
        return (position / self.zoom) + self.position
