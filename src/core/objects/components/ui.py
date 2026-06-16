import logging
from typing import Optional
import gc

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.objects.game_object import GameObject
from src.core.objects.components import PositionComponent

from src.core.objects.event import Event
from src.core.systems.input import cursor

DEFAULT_DIALOG_COLOR = (150, 150, 150)

class UITransform:
    """
        Область интерфейса.

        UITransform может использоваться как компонент UIControl
        или как внутренний элемент объекта интерфейса,
        связанного с 2D объектом GameObject.
    """
    def __init__(
            self,
            position: Vector2,
            size: Vector2,
            screen_anchor: bool = True,
            anchor: Optional[GameObject] = None,
            centred: bool = False,
            parent: Optional['UITransform'] = None,
            children: set['UITransform'] = set()
    ):
        self._position = position
        self._original_position = position.copy()
        self.screen_anchor: bool = screen_anchor
        self.anchor = anchor
        self.size = size
        self.centred = centred
        self.parent = parent
        self.fit_anchor()
        self.children: set['UITransform'] = children

    @property
    def position(self):
        if self.centred:
            return self._position - self.size // 2
        else:
            return self._position

    @position.setter
    def position(self, value):
        if self.centred:
            self._position = value + self.size // 2
        else:
            self._position = value

    def add_child(self, child: 'UITransform'):
        self.children.add(child)
        child.parent = self

    def remove_child(self, child: 'UITransform'):
        self.children.remove(child)
        child.parent = None

    def update(self, delta_time):
        self.fit_anchor()

    def fit_anchor(self):
        if self.anchor and not self.screen_anchor:
            self._position = self._original_position.copy()
            if self.anchor.has(PositionComponent):
                self._position += self.anchor.get(PositionComponent).position
            elif self.anchor.has(UITransform):
                self._position += self.anchor.get(UITransform).position
        

    def contains(self, mouse_x, mouse_y) -> bool:
        """Проверка координат на вхождение в зону нажатия."""
        return (
            mouse_x > self.position.x
            and mouse_x < self.position.x + self.size.x
            and mouse_y > self.position.y
            and mouse_y < self.position.y + self.size.y
        )

class ClickHandlerComponent:
    """Контроллер кликов."""
    def __init__(self, ui_transform: UITransform):
        self.ui_transform = ui_transform
        self.on_button_pressed: Event = Event()
        cursor.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self):
        # logging.debug(f"Левый клик {id(self)} {gc.get_referrers(self)}")
        cursor_pos = None
        if self.ui_transform.screen_anchor:
            cursor_pos = cursor.pos
        else:
            cursor_pos = cursor.global_pos
        if self.ui_transform.contains(cursor_pos.x, cursor_pos.y):
            self.on_button_pressed.emit()

    def free(self):
        cursor.on_left_click.unsubscribe(self.on_left_click)

DEFAULT_TEXT_COLOR = (255, 255, 255)

class TextRenderComponent:
    """Отрисовщик текста."""
    def __init__(self, text: str, size: int, color: tuple = DEFAULT_TEXT_COLOR):
        self.text = text
        self.size = size
        self.color = color

    def set_text(self, text: str):
        self.text = str(text)

    def draw(self, screen: pygame.Surface, size, local_position, zoom):
        font = (
            pygame.font
            .SysFont("Arial", self.size)
            .render(self.text, True, self.color)
        )
        screen.blit(font, local_position)

class VerticalLayoutComponent:
    """Организатор вертикального списка (сверху-вниз)."""
    def __init__(self, ui_transform: UITransform, space: int = 10):
        self.ui_transform = ui_transform
        self.space = space

    def update(self, delta_time):
        y_offset = self.space
        for child in self.ui_transform.children:
            child.position.y = y_offset
            y_offset += child.size.y + self.space

class UIControl(GameObject):
    """Универсальный элемент интерфейса."""
    def __init__(self):
        super().__init__()
        self.z_index = 1000