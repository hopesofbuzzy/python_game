import logging
from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.objects.event import Event
from src.core.singletones.event_bus import event_bus


@dataclass
class Cursor:
    """
        Объект мыши с данными о состоянии.
    """

    pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    global_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    rel_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    buttons: list = field(default_factory=lambda: [0, 0, 0])

cursor = Cursor()

class InputManager:
    def __init__(self):
        self.on_exit = Event()

    def handle_input(self, scene, camera):
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEMOTION:
                    cursor.pos = Vector2(event.dict["pos"])
                    cursor.global_pos = camera.to_global(cursor.pos)
                    cursor.rel_pos = event.dict["rel"]
                    cursor.buttons = list(event.dict["buttons"])
                case pygame.MOUSEBUTTONDOWN:
                    if event.dict["button"] - 1 in range(0, 3):
                        cursor.buttons[event.dict["button"] - 1] = 1
                        if event.dict["button"] == 1:
                            event_bus.fire("on_mouse_left_click", cursor)
                case pygame.MOUSEBUTTONUP:
                    if event.dict["button"] - 1 in range(0, 3):
                        cursor.buttons[event.dict["button"] - 1] = 0
                case pygame.MOUSEWHEEL:
                    logging.debug(event)
                    if event.dict["y"] == 1:
                        event_bus.fire("on_mouse_wheel", True)
                    else:
                        event_bus.fire("on_mouse_wheel", False)
                case pygame.QUIT:
                    self.on_exit.emit()
            for object in scene.object_registry.values():
                object.handle_input(event, cursor)