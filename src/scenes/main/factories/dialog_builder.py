import logging

from pygame.math import Vector2

from src.core.objects import (
    UITransform,
    UIControl,
    TextRenderComponent,
    VerticalLayoutComponent,
    ClickHandlerComponent,
    RectComponent,
    PanelRendererComponent
)

from src.scenes.main.objects import BarComponent

from src.scenes.main.factories.ui_factory import UIFactory

DEFAULT_DIALOG_COLOR = (150, 150, 150)
DIALOG_OBJECTS_SPACE = 10

class DialogBuilder:
    def __init__(self, add_object, ui_factory: UIFactory):
        self.add_object = add_object
        self.ui_factory = ui_factory
        self._dialog = None

    def with_dialog(
        self,
        position: Vector2,
        size: Vector2,
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
            Vector2(0, 0),
            self._dialog,
            text,
            size
        )
        self._dialog.add_child(text)
        return self

    def build(self):
        if not self._dialog:
            raise ValueError("Сперва постройте диалог")
        return self._dialog
