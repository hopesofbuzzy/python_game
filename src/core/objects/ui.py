import logging
from dataclasses import dataclass, field

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.systems.event import Event
from src.core.objects.game_object import (
    Model,
    View,
    Controller,
    GameObject
)
from src.core.objects.view import RectView

DEFAULT_DIALOG_COLOR = (150, 150, 150)

@dataclass
class ButtonModel(Model):
    # Модель содержит конкретную область клика.
    # size в ButtonView отвечает чисто за визуал!
    size: Vector2 = field(default_factory=lambda: Vector2(35, 35))
    is_pressed: bool = False

    def contains(self, mouse_x, mouse_y) -> bool:
        """Проверка координат на вхождение в зону нажатия."""
        return (
            mouse_x > self.position.x
            and mouse_x < self.position.x + self.size.x
            and mouse_y > self.position.y
            and mouse_y < self.position.y + self.size.y
        )

    def press(self):
        """Нажатие кнопки."""
        self.is_pressed = True
        logging.debug("Кнопка нажата!")

@dataclass
class ButtonView(RectView):
    size: Vector2 = field(default_factory=lambda: Vector2(35, 35))
    centred: bool = False

@dataclass
class ButtonController(Controller):
    on_button_pressed: Event = field(default_factory=lambda: Event())

    def __post_init__(self):
        self.cursor.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self, cursor):
        cursor_pos = cursor.global_pos
        if self.model.contains(cursor_pos.x, cursor_pos.y):
            self.model.press()
            self.on_button_pressed.emit()

@dataclass
class Button(GameObject[ButtonModel, View, ButtonController]):
    ...

@dataclass
class DialogModel(Model):
    text: str = ""
    button: Button = field(default_factory=lambda: Button(
        model=ButtonModel(local_position=Vector2(0, -30)),
    ))

    on_ok_pressed: Event = field(default_factory=lambda: Event())

    def __post_init__(self):
        self.button.model.on_button_pressed.subscribe(
            lambda: self.on_ok_pressed.emit()
        )

@dataclass
class DialogView(View):
    color: tuple[int, int, int] = DEFAULT_DIALOG_COLOR
    size: Vector2 = field(default_factory=lambda: Vector2(200, 100))
    centred: bool = False

    def get_centred_local_position(self, local_position, zoom):
        return local_position - (self.size * zoom // 2)

    def draw(self, screen: pygame.Surface, model: Model, local_position, zoom):
        if self.centred:
            local_position = self.get_centred_local_position(local_position, zoom)
        rect = pygame.Rect(
            local_position.x,
            local_position.y,
            self.size.x * zoom,
            self.size.y * zoom
        )
        pygame.draw.rect(screen, self.color, rect)

@dataclass
class Dialog(GameObject[DialogModel, DialogView, Controller]):
    ...