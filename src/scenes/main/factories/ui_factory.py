import logging

from pygame.math import Vector2

from src.core.objects import (
    ClickHandlerComponent,
    PanelRendererComponent,
    TextRenderComponent,
    UIControl,
    UITransform,
)
from src.scenes.main.objects import BarComponent

DEFAULT_BUTTON_COLOR = (120, 120, 120)
DEFAULT_TEXT_CONTAINER_SIZE = Vector2(100, 10)
DEFAULT_TEXT_SIZE = 18

class UIFactory:
    """Фабрика элементов интерфейса."""

    def __init__(self, add_object):
        self.add_object = add_object

    def create_text(
        self,
        text: str,
        position: Vector2,
        size: int = DEFAULT_TEXT_SIZE,
        container_size: Vector2 = DEFAULT_TEXT_CONTAINER_SIZE,
        anchor = None
    ):
        text_control = (
            UIControl()
            .add(UITransform(position, container_size, anchor))
            .add(TextRenderComponent(text, size))
        )
        self.add_object(text_control)
        return text_control

    def create_bar(self, position, size, start, max, anchor = None):
        bar = (
            UIControl()
            .add(UITransform(position, size, anchor, True))
            .add(BarComponent(start, max))
        )
        self.add_object(bar)
        return bar

    def create_click_handler(
            self,
            position: Vector2,
            size: Vector2,
            anchor = None,
            centred: bool = True
    ):
        click_handler = (
            UIControl()
            .add(UITransform(
                    position,
                    size,
                    anchor,
                    centred=centred
            ))
        )
        click_handler.add(ClickHandlerComponent(click_handler))
        self.add_object(click_handler)
        return click_handler

    def create_button(
            self,
            text: str,
            font_size: int,
            position: Vector2,
            size: Vector2,
            anchor,
            color: tuple = DEFAULT_BUTTON_COLOR
    ):
        button = self.create_click_handler(position, size, anchor, centred=False)
        button.add(PanelRendererComponent(color))
        button.add(TextRenderComponent(text, font_size))
        return button