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

    def create_text(self, text, size):
        text = (
            UIControl()
            .add(UITransform(Vector2(100, 0), Vector2(100, 100), True))
            .add(TextRenderComponent(text, size))
        )
        self.add_object(text)
        return text

    def create_bar(self, position, size, start, max, anchor = None):
        bar = (
            UIControl()
            .add(UITransform(position, size, False, anchor, True))
            .add(BarComponent(start, max))
        )
        self.add_object(bar)
        return bar

    def create_dialog(self, plant_model):
        ...
