import logging

from pygame.math import Vector2

from src.core.objects import (
    UITransform,
    UIControl,
    TextRenderComponent,
    ClickHandlerComponent,
)

from src.scenes.main.objects import BarComponent

class UIFactory:
    """Фабрика элементов интерфейса."""

    def __init__(self, add_object):
        self.add_object = add_object

    def create_text(self, position, anchor, text, size):
        text = (
            UIControl()
            .add(UITransform(position, Vector2(100, 10), anchor))
            .add(TextRenderComponent(text, size))
        )
        self.add_object(text)
        return text

    def create_bar(self, position, size, start, max, anchor = None):
        bar = (
            UIControl()
            .add(UITransform(position, size, anchor, True))
            .add(BarComponent(start, max))
        )
        self.add_object(bar)
        return bar

    def create_click_handler(self, position, size, anchor):
        click_handler = (
            UIControl()
            .add(UITransform(
                    position,
                    size,
                    anchor,
                    centred=True
            ))
        )
        click_handler.add(ClickHandlerComponent(click_handler))
        self.add_object(click_handler)
        return click_handler