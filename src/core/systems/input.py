import logging
from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.objects.event import Event


@dataclass
class Cursor:
    """
        Объект мыши с данными о состоянии.

        Args:
            on_left_click(),
            on_mouse_wheel_up(),
            on_mouse_wheel_down()
    """

    pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    global_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    rel_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    buttons: list = field(default_factory=lambda: [0, 0, 0])

    on_left_click: Event = field(default_factory=lambda: Event())
    on_mouse_wheel: Event = field(default_factory=lambda: Event())

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
                            cursor.on_left_click.emit()
                case pygame.MOUSEBUTTONUP:
                    if event.dict["button"] - 1 in range(0, 3):
                        cursor.buttons[event.dict["button"] - 1] = 0
                case pygame.MOUSEWHEEL:
                    logging.debug(event)
                    if event.dict["y"] == 1:
                        cursor.on_mouse_wheel.emit(True)
                    else:
                        cursor.on_mouse_wheel.emit(False)
                case pygame.QUIT:
                    self.on_exit.emit()
            for object in scene.object_registry.values():
                object.handle_input(event)