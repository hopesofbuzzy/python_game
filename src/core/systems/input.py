import logging
from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.systems.event import Event


@dataclass
class Cursor:
    """
        Объект мыши с данными о состоянии.

        Args:
            on_left_click(cursor),
            on_mouse_wheel_up(),
            on_mouse_wheel_down()
    """

    pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    global_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    rel_pos: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    buttons: list = field(default_factory=lambda: [0, 0, 0])

    on_left_click: Event = field(default_factory=lambda: Event())
    on_mouse_wheel: Event = field(default_factory=lambda: Event())

class InputManager:
    def __init__(self):
        self.cursor = Cursor()
        self.on_exit = Event()

    def handle_input(self, scene, camera):
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEMOTION:
                    self.cursor.pos = Vector2(event.dict["pos"])
                    self.cursor.global_pos = camera.to_global(self.cursor.pos)
                    self.cursor.rel_pos = event.dict["rel"]
                    self.cursor.buttons = list(event.dict["buttons"])
                case pygame.MOUSEBUTTONDOWN:
                    if event.dict["button"] - 1 in range(0, 3):
                        self.cursor.buttons[event.dict["button"] - 1] = 1
                        if event.dict["button"] == 1:
                            self.cursor.on_left_click.emit(self.cursor)
                case pygame.MOUSEBUTTONUP:
                    if event.dict["button"] - 1 in range(0, 3):
                        self.cursor.buttons[event.dict["button"] - 1] = 0
                case pygame.MOUSEWHEEL:
                    logging.debug(event)
                    if event.dict["y"] == 1:
                        self.cursor.on_mouse_wheel.emit(True)
                    else:
                        self.cursor.on_mouse_wheel.emit(False)
                case pygame.QUIT:
                    self.on_exit.emit()
            for object in scene.object_registry.values():
                if object.controller:
                    object.controller.handle_input(event)
