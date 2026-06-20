import logging

from pygame.math import Vector2

from src.core.objects import (
    ClickHandlerComponent,
    PanelRendererComponent,
    TextRenderComponent,
    UIControl,
    UITransform,
    VerticalLayoutComponent
)
from src.scenes.main.objects import BarComponent

DEFAULT_BUTTON_COLOR = (120, 120, 120)
DEFAULT_BUTTON_INPUT_PRIORITY = 1000
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
        """Создаёт текст в виде объекта интерфейса."""
        text_control = (
            UIControl()
            .add(UITransform(position, container_size, anchor))
            .add(TextRenderComponent(text, size))
        )
        self.add_object(text_control)
        return text_control

    def create_bar(self, position, size, start, max, anchor = None):
        """Создаёт шкалу в виде объекта интерфейса."""
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
            centred: bool = True,
            input_priority: int = 5
    ):
        """
            Обработчик кликов. В одиночку обычно используется для кликабельных объектов
            мира, а не для интерфейса.
        """
        click_handler = (
            UIControl()
            .add(UITransform(
                    position,
                    size,
                    anchor,
                    centred=centred
            ))
        )
        click_handler.add(ClickHandlerComponent(click_handler, input_priority))
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
        """
            Кнопка интерфейса.

            input_priority: 1
        """
        button = self.create_click_handler(
            position,
            size,
            anchor,
            centred=False,
            input_priority=DEFAULT_BUTTON_INPUT_PRIORITY
        )
        button.add(PanelRendererComponent(color))
        button.add(TextRenderComponent(text, font_size))
        return button

    def create_vertical_container(self, position, size, anchor, color):
        """Создаёт вертикальный контейнер (сверху-вниз) для объектов интерфейса."""
        inventory = (
            UIControl()
            .add(UITransform(
                position,
                size,
                anchor
            ))
            .add(PanelRendererComponent(color))
        )
        inventory.add(VerticalLayoutComponent(inventory))

    def create_image(self, position, size, image_path):
        """Создаёт картинку в виде объекта интерфейса."""
        inventory = (
            UIControl()
            .add(UITransform(
                position,
                size
            ))
        )