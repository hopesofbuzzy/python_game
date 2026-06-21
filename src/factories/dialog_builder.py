import logging
from typing import Callable

from pygame.math import Vector2

from src.core.objects import (
    ClickHandlerComponent,
    PanelRendererComponent,
    RectComponent,
    TextRenderComponent,
    UIControl,
    UITransform,
    VerticalLayoutComponent,
)
from src.core.singletones.event_bus import EventBus
from src.factories.ui_factory import UIFactory
from src.scenes.main.objects import BarComponent

DEFAULT_DIALOG_COLOR = (150, 150, 150)
DIALOG_OBJECTS_SPACE = 10
DEFAULT_BUTTON_COLOR = (120, 120, 120)
DEFAULT_DIALOG_SIZE = Vector2(250, 150)
DEFAULT_BUTTON_POSITION = Vector2(0, 0)
DEFAULT_BUTTON_SIZE = Vector2(100, 35)
DEFAULT_DIALOG_TEXT_CONTAINER_SIZE = Vector2(120, 80)

class DialogBuilder:
    def __init__(self, add_object, ui_factory: UIFactory, event_bus: EventBus):
        self.add_object = add_object
        self.ui_factory = ui_factory
        self.event_bus = event_bus
        self._dialog = None

    def with_dialog(
        self,
        position: Vector2,
        size: Vector2 = DEFAULT_DIALOG_SIZE,
        anchor=None,
        color: tuple = DEFAULT_DIALOG_COLOR
    ):
        dialog = (
            UIControl()
            .add(UITransform(
                position,
                size,
                anchor
            ))
            .add(PanelRendererComponent(color))
        )
        dialog.add(VerticalLayoutComponent(
            dialog, DIALOG_OBJECTS_SPACE
        ))
        self.add_object(dialog)
        self._dialog = dialog
        return self

    def with_text(
        self,
        text,
        size
    ):
        if not self._dialog:
            raise ValueError("Сперва постройте диалог")
        text = self.ui_factory.create_text(
            text,
            Vector2(0, 0),
            size,
            DEFAULT_DIALOG_TEXT_CONTAINER_SIZE,
            self._dialog,
        )
        self._dialog.add_child(text)
        return self

    def with_button(
        self,
        text: str,
        font_size: int,
        data = None,
        position: Vector2 = DEFAULT_BUTTON_POSITION,
        size: Vector2 = DEFAULT_BUTTON_SIZE,
        color: tuple = DEFAULT_BUTTON_COLOR,
    ):
        if not self._dialog:
            raise ValueError("Сперва постройте диалог")
        button = self.ui_factory.create_button(
            text,
            font_size,
            position,
            size,
            self._dialog,
            color,
            data=data
        )
        logging.debug("Функция соединена")
        button.get(ClickHandlerComponent).on_button_pressed.subscribe(
            lambda data: self.event_bus.fire("on_requested_upgrade", data)
        )
        self._dialog.add_child(button)
        return self

    def build(self):
        if not self._dialog:
            raise ValueError("Сперва постройте диалог")
        return self._dialog
