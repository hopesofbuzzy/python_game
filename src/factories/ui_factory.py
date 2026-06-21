from collections.abc import Callable

from pygame.math import Vector2

from src.core.objects import (
    ClickHandlerComponent,
    ContainerComponent,
    ImageRendererComponent,
    MouseHoverComponent,
    PanelRendererComponent,
    TextRenderComponent,
    UIControl,
    UITransform,
    VerticalLayoutComponent,
)
from src.core.singletones.event_bus import EventBus
from src.scenes.main.objects import BarComponent

DEFAULT_BUTTON_COLOR = (120, 120, 120)
DEFAULT_BUTTON_INPUT_PRIORITY = 1000
DEFAULT_TEXT_CONTAINER_SIZE = Vector2(100, 10)
DEFAULT_TEXT_SIZE = 18
DEFAULT_TEXT_LINESPACE = 0
DEFAULT_TOOLTIP_COLOR = (60, 60, 60)


class UIFactory:
    """Фабрика элементов интерфейса."""

    def __init__(self, add_object: Callable, event_bus: EventBus):
        self.add_object = add_object
        self.event_bus = event_bus

    def create_text(
        self,
        text: str,
        position: Vector2,
        size: int = DEFAULT_TEXT_SIZE,
        container_size: Vector2 = DEFAULT_TEXT_CONTAINER_SIZE,
        anchor=None,
        linespace=DEFAULT_TEXT_LINESPACE,
    ):
        """Создаёт текст в виде объекта интерфейса."""
        text_control = (
            UIControl()
            .add(UITransform(position, container_size, anchor))
            .add(TextRenderComponent(text, size))
        )
        self.add_object(text_control)
        return text_control

    def create_bar(self, position, size, start, max, anchor=None):
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
        anchor=None,
        centred: bool = True,
        input_priority: int = 5,
        data=None,
    ):
        """
            Обработчик кликов. В одиночку обычно
            используется для кликабельных объектов
            мира, а не для интерфейса.
        """
        click_handler = UIControl().add(
            UITransform(position, size, anchor, centred=centred)
        )
        click_handler.add(
            ClickHandlerComponent(click_handler, input_priority, data)
        )
        self.add_object(click_handler)
        return click_handler

    def create_button(
        self,
        text: str,
        font_size: int,
        position: Vector2,
        size: Vector2,
        anchor,
        color: tuple = DEFAULT_BUTTON_COLOR,
        data=None,
    ):
        """
        Кнопка интерфейса, выдающая данные по нажатию.

        input_priority: 1
        """
        button = self.create_click_handler(
            position,
            size,
            anchor,
            centred=False,
            input_priority=DEFAULT_BUTTON_INPUT_PRIORITY,
            data=data,
        )
        button.add(PanelRendererComponent(color))
        button.add(TextRenderComponent(text, font_size))
        self.add_object(button)
        return button

    def create_vertical_container(self, position, size, anchor, color, space):
        """
            Создаёт вертикальный контейнер (сверху-вниз)
            для объектов интерфейса.
        """
        conatiner = (
            UIControl()
            .add(UITransform(position, size, anchor))
            .add(PanelRendererComponent(color))
        )
        conatiner.add(VerticalLayoutComponent(conatiner, space))
        self.add_object(conatiner)
        return conatiner

    def create_empty_container(self, position, size, anchor=None):
        """Создаёт пустой контейнер (без порядка) для объектов интерфейса."""
        conatiner = UIControl().add(UITransform(position, size, anchor))
        conatiner.add(ContainerComponent(conatiner))
        self.add_object(conatiner)
        return conatiner

    def create_image(self, position, size, image_path, anchor=None, data=None):
        """Создаёт кликабельную картинку в виде объекта интерфейса."""
        image = self.create_click_handler(
            position,
            size,
            anchor,
            centred=False,
            input_priority=DEFAULT_BUTTON_INPUT_PRIORITY,
            data=data,
        )
        image.add(ImageRendererComponent(image_path))
        self.add_object(image)
        return image

    def create_tooltip_message(
        self,
        position,
        size,
        text_size,
        text,
        anchor=None,
        color=DEFAULT_BUTTON_COLOR,
    ):
        tooltip_message = (
            UIControl()
            .add(UITransform(position, size, anchor))
            .add(PanelRendererComponent(color))
            .add(
                TextRenderComponent(
                    text, text_size, linespace=DEFAULT_TEXT_LINESPACE
                )
            )
        )
        self.add_object(tooltip_message)
        return tooltip_message

    def create_tooltip(
        self,
        position,
        size,
        text,
        anchor=None,
    ):
        tooltip = UIControl().add(UITransform(position, size, anchor))
        mouse_hover_comp = MouseHoverComponent(tooltip, text)
        tooltip.add(mouse_hover_comp)
        mouse_hover_comp.on_mouse_entered.subscribe(
            lambda text, cursor_local_pos: self.event_bus.fire(
                "on_tooltip_requested", text, cursor_local_pos
            )
        )
        mouse_hover_comp.on_mouse_exited.subscribe(
            lambda text: self.event_bus.fire("on_tooltip_hide_requested", text)
        )
        self.add_object(tooltip)
        return tooltip
