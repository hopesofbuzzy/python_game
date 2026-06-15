import logging
from dataclasses import dataclass, field

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.objects.game_object import GameObject
from src.core.objects.event import Event
from src.core.systems.input import cursor

DEFAULT_DIALOG_COLOR = (150, 150, 150)

class UITransformComponent:
    def __init__(self, position: Vector2, size: Vector2):
        self.position = position
        self.size = size

    def contains(self, mouse_x, mouse_y) -> bool:
        """Проверка координат на вхождение в зону нажатия."""
        return (
            mouse_x > self.position.x
            and mouse_x < self.position.x + self.size.x
            and mouse_y > self.position.y
            and mouse_y < self.position.y + self.size.y
        )

class ButtonControllerComponent:
    def __init__(self, ui_size: UITransformComponent):
        self.ui_size = ui_size
        self.is_button_pressed: bool = False
        self.on_button_pressed: Event = Event()
        cursor.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self):
        cursor_pos = cursor.global_pos
        if self.ui_size.contains(cursor_pos.x, cursor_pos.y):
            self.on_button_pressed.emit()

class TextComponent:
    def __init__(self, text: str):
        self.text = text

    def draw(self, screen: pygame.Surface, model, local_position, zoom):
        ...

class Button(GameObject):
    def __init__(self, position, ui_transform, view, controller):
        self.ui_transform = ui_transform
        super().__init__(position, view, controller)
        self.on_button_pressed: Event = Event()
        self.controller.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self):
        self.on_button_pressed.emit()

# class DialogControllerComponent(Model):
#     text: str = ""
#     button: Button = field(default_factory=lambda: Button(
#         model=ButtonModel(local_position=Vector2(0, -30)),
#     ))

#     on_ok_pressed: Event = field(default_factory=lambda: Event())

#     def __post_init__(self):
#         self.button.model.on_button_pressed.subscribe(
#             lambda: self.on_ok_pressed.emit()
#         )

# @dataclass
# class DialogView(View):
#     color: tuple[int, int, int] = DEFAULT_DIALOG_COLOR
#     size: Vector2 = field(default_factory=lambda: Vector2(200, 100))
#     centred: bool = False

#     def get_centred_local_position(self, local_position, zoom):
#         return local_position - (self.size * zoom // 2)

#     def draw(self, screen: pygame.Surface, model: Model, local_position, zoom):
#         if self.centred:
#             local_position = self.get_centred_local_position(local_position, zoom)
#         rect = pygame.Rect(
#             local_position.x,
#             local_position.y,
#             self.size.x * zoom,
#             self.size.y * zoom
#         )
#         pygame.draw.rect(screen, self.color, rect)


class Dialog(GameObject):
    def __init__(self, position, ui_transform, view, controller):
        self.ui_transform = ui_transform
        super().__init__(position, view, controller)
        self.on_button_pressed: Event = Event()
        self.controller.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self):
        self.on_button_pressed.emit()