import gc
import logging
from typing import Optional

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.objects.components import PositionComponent
from src.core.objects.event import Event
from src.core.objects.game_object import GameObject
from src.core.singletones.event_bus import EventFlow, event_bus
from src.core.singletones.image_loader import Image
from src.core.singletones.image_loader import image_loader as il
from src.core.systems.input import Cursor

DEFAULT_DIALOG_COLOR = (150, 150, 150)
DEFAULT_UI_Z_INDEX = 1000

class UITransform:
    """
        Область интерфейса.

        ВАЖНО: UITransform и все компоненты интерфейса должны
        использоваться только как компоненты объекта интерфейса - UIControl.

        Для привязки элемента интерфейса к объекту мира
        нужно использовать object.add_child(ui_control) и anchor = object.

        Без anchor UITransform всегда работает с координатами экрана.
    """
    def __init__(
            self,
            position: Vector2,
            size: Vector2,
            anchor: Optional[GameObject] = None,
            centred: bool = False,
    ):
        self.original_position = position.copy()
        self.local_position = self.original_position
        self.anchor = anchor
        self.size = size
        self.centred = centred
        # Позволяет контейнеру регулировать отрисовку при anchor.
        self._position_screen_resize = True

    @property
    def position(self):
        if self.centred:
            result = self.local_position.copy() - self.size // 2
        else:
            result = self.local_position.copy()
        result += self.get_anchor_position()
        return result

    @position.setter
    def position(self, value):
        if self.centred:
            self.local_position = value + self.size // 2
        else:
            self.local_position = value
        self.local_position -= self.get_anchor_position()

    def get_anchor_position(self) -> Vector2:
        if self.anchor:
            if self.anchor.has(PositionComponent):
                return self.anchor.get(PositionComponent).position
            elif self.anchor.has(UITransform):
                return self.anchor.get(UITransform).position
        return Vector2(0, 0)

    def contains(self, mouse_x, mouse_y) -> bool:
        """Проверка координат на вхождение в зону нажатия."""
        return (
            mouse_x > self.position.x
            and mouse_x < self.position.x + self.size.x
            and mouse_y > self.position.y
            and mouse_y < self.position.y + self.size.y
        )

DEFAULT_TEXT_COLOR = (255, 255, 255)
DEFAULT_TEXT_LINESPACE = 0

class TextRenderComponent:
    """Отрисовщик текста."""
    def __init__(
        self,
        text: str,
        size: int,
        color: tuple = DEFAULT_TEXT_COLOR,
        linespace: int = DEFAULT_TEXT_LINESPACE
    ):
        self.size = size
        self.color = color
        self.parsed_text = self.parse_text(text)
        self.linespace = linespace
        self._surfaces: list = list()
        self._font = pygame.font.SysFont("Arial", self.size)
        self._cached_text: str = text
        self._converted: bool = False
        self.render_text()

    def set_text(self, text: str):
        self.parsed_text = self.parse_text(text)
        if text != self._cached_text:
            self.render_text()

    def render_text(self):
        self._surfaces = list()
        for text_part in self.parsed_text:
            self._surfaces.append(
                self._font.render(text_part, True, self.color).convert_alpha()
            )
        self._converted = False

    def parse_text(self, text):
        return text.split("\n")

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        y_offset = 0
        for surface in self._surfaces:
            screen.blit(surface, local_position + Vector2(0, y_offset))
            y_offset += self.linespace + surface.get_size()[1]

class PanelRendererComponent:
    """Отрисовщик панели интерфейса (не зависит от зума)."""
    def __init__(self, color: tuple = DEFAULT_TEXT_COLOR):
        self.color = color

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        rect = pygame.Rect(
            local_position.x,
            local_position.y,
            size.x,
            size.y
        )
        pygame.draw.rect(screen, self.color, rect)

class ImageRendererComponent:
    """Отрисовщик картинки."""
    def __init__(self, image_path: str):
        self._original_image: Image = il.load_image(image_path)
        self._scaled_image = None

    def get_scaled_image(self, size: tuple):
        if not self._scaled_image:
            if isinstance(self._original_image, Image):
                self._scaled_image = pygame.transform.scale(
                    self._original_image.surface, size=size
                )
        return self._scaled_image

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        image = self.get_scaled_image(tuple(size))
        if image:
            screen.blit(image, local_position)

class UIControl(GameObject):
    """Универсальный элемент интерфейса."""
    def __init__(self):
        super().__init__()
        self.z_index = DEFAULT_UI_Z_INDEX

class ClickHandlerComponent:
    """Контроллер кликов, выдающий данные по нажатию."""
    def __init__(self, ui_control: UIControl, input_priority=5, data=None):
        self.ui_transform = ui_control.get(UITransform)
        self.on_button_pressed: Event = Event()
        self.data = data
        event_bus.subscribe(
            "on_mouse_left_click",
            self.on_mouse_left_click,
            priority=input_priority
        )

    def on_mouse_left_click(self, event: EventFlow, cursor):
        cursor_pos = None
        if self.ui_transform.anchor:
            cursor_pos = cursor.global_pos
        else:
            cursor_pos = cursor.pos
        if self.ui_transform.contains(cursor_pos.x, cursor_pos.y):
            logging.debug("ClickHandlerComponent was clicked")
            self.on_button_pressed.emit(self.data)
            event.stop()

class MouseHoverComponent:
    """Контроллер проверки движения мыши по элементу."""
    def __init__(self, ui_control: UIControl, data=None):
        self.ui_transform = ui_control.get(UITransform)
        self.is_mouse_inside: bool = False
        self.on_mouse_entered: Event = Event()
        self.on_mouse_exited: Event = Event()
        self.data = data

    def handle_input(self, event: PygameEvent, cursor: Cursor):
        cursor_pos = None
        if self.ui_transform.anchor:
            cursor_pos = cursor.global_pos
        else:
            cursor_pos = cursor.pos
        is_mouse_inside = self.ui_transform.contains(cursor_pos.x, cursor_pos.y)
        if self.is_mouse_inside and not is_mouse_inside:
            
            self.on_mouse_exited.emit(self.data)
            self.is_mouse_inside = False
        if not self.is_mouse_inside and is_mouse_inside:
            logging.info("Вход в зону")
            self.on_mouse_entered.emit(self.data, cursor.pos)
            self.is_mouse_inside = True



class VerticalLayoutComponent:
    """Организатор вертикального списка (сверху-вниз)."""
    def __init__(self, ui_control: UIControl, space: int = 10):
        self.ui_control = ui_control
        self.space = space

    def update(self, delta_time):
        if not self.ui_control.get(UITransform).anchor:
            y_offset = self.ui_control.get(UITransform).position.y + self.space
        else:
            y_offset = self.space
        for child in self.ui_control.children:
            child.get(UITransform)._position_screen_resize = False
            if child.has(UITransform):
                child.get(UITransform).local_position = (
                    child.get(UITransform).original_position + Vector2(0, y_offset)
                )
                y_offset += child.get(UITransform).size.y + self.space

class ContainerComponent:
    """Контейнер, выравнивающий позиции объектов относительно своей."""
    def __init__(self, ui_control: UIControl):
        self.ui_control = ui_control

    def update(self, delta_time):
        if not self.ui_control.get(UITransform).anchor:
            origin = self.ui_control.get(UITransform).position
        else:
            origin = Vector2(0, 0)
        for child in self.ui_control.children:
            child.get(UITransform)._position_screen_resize = False
            if child.has(UITransform):
                child.get(UITransform).local_position = (
                    child.get(UITransform).original_position + origin
                )