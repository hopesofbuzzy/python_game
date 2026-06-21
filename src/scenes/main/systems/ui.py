import logging
from typing import Callable

from pygame.math import Vector2

from src.config.plants import PLANTS_DESCRIPTIONS, PLANTS_PRICES
from src.config.generator_config import *
from src.core.objects import ClickHandlerComponent, TextRenderComponent
from src.core.objects.event import Event
from src.core.singletones.event_bus import EventBus, EventFlow
from src.factories.ui_factory import UIFactory
from src.scenes.main.objects.components.inventory import Slot
from src.scenes.main.systems.currency import CurrencyManager

SUNS_TEXT_POSITION = Vector2(0, 0)
SUNS_TEXT_SIZE = 25
WAVE_NUMBER_TEXT_POSITION = SUNS_TEXT_POSITION + Vector2(0, 20)
WAVE_NUMBER_TEXT_SIZE = 25
TIME_BEFORE_WAVE_TEXT_POSITION = WAVE_NUMBER_TEXT_POSITION + Vector2(0, 30)
TIME_BEFORE_WAVE_TEXT_SIZE = 15
INVENTORY_POSITION = TIME_BEFORE_WAVE_TEXT_POSITION + Vector2(0, 300)
INVENTORY_SIZE = Vector2(60, 300)
INVENTORY_COLOR = (150, 150, 150)
SEED_TEXT_POSITION = Vector2(0, INVENTORY_POSITION.y + INVENTORY_SIZE.y)
SEED_TEXT_SIZE = 20
SLOT_SIZE = Vector2(60, 65)
SLOT_COLOR = (100, 100, 100)
TOOLTIP_TEXT_FONT_SIZE = 20

class UIManager:
    """Менеджер интерфейса игры (HUD)"""
    def __init__(
        self,
        ui_factory: UIFactory,
        currency: CurrencyManager,
        event_bus: EventBus,
        get_time_before_wave_func: Callable,
        inventory_slots: list[Slot]
    ):
        self.ui_factory = ui_factory
        self.currency = currency
        self.get_time_before_wave = get_time_before_wave_func
        self.build_stats()
        self.build_inventory(inventory_slots)
        self.event_bus = event_bus
        self.event_bus.subscribe("on_wave_started", self.on_wave_started)
        # Tooltip
        self.event_bus.subscribe("on_tooltip_requested", self.show_tooltip)
        self.event_bus.subscribe("on_tooltip_hide_requested", self.hide_tooltip)
        self.tooltip = None
        
    def build_stats(self):
        self.suns_text = self.ui_factory.create_text(
            f"Солнышки: {self.currency.suns}",
            SUNS_TEXT_POSITION,
            SUNS_TEXT_SIZE
        )
        self.currency.on_suns_update.subscribe(
            lambda s: self.suns_text.get(TextRenderComponent).set_text(f"Солнышки: {s}")
        )
        self.wave_number = self.ui_factory.create_text(
            f"Текущая волна: ...",
            WAVE_NUMBER_TEXT_POSITION,
            WAVE_NUMBER_TEXT_SIZE
        )
        self.time_before_wave = self.ui_factory.create_text(
            f"Следующая волна через: ...",
            TIME_BEFORE_WAVE_TEXT_POSITION,
            TIME_BEFORE_WAVE_TEXT_SIZE
        )
        self.seed = self.ui_factory.create_text(
            f"Зерно генерации: {seed}",
            SEED_TEXT_POSITION,
            SEED_TEXT_SIZE
        )

    def build_inventory(self, inventory_slots: list[Slot]):
        container = self.ui_factory.create_vertical_container(
            INVENTORY_POSITION, INVENTORY_SIZE, None, INVENTORY_COLOR, 5
        )
        for slot in inventory_slots:
            inner_container = self.ui_factory.create_vertical_container(
                Vector2(0, 0), SLOT_SIZE, None, SLOT_COLOR, -5
            )
            image_container = self.ui_factory.create_empty_container(
                Vector2(0, 0), SLOT_SIZE
            )
            image = self.ui_factory.create_image(
                Vector2(0, 0), Vector2(60, 60), slot.image_path, data=slot
            )
            image.get(ClickHandlerComponent).on_button_pressed.subscribe(
                lambda clicked_slot: self.event_bus.fire(
                    "on_inventory_changed_slot",
                    clicked_slot
                )
            )
            tooltip = self.ui_factory.create_tooltip(
                Vector2(0, 0,),
                SLOT_SIZE,
                PLANTS_DESCRIPTIONS[slot.name]
            )
            image_container.add_child(image)
            image_container.add_child(tooltip)
            inner_container.add_child(image_container)
            inner_container.add_child(
                self.ui_factory.create_text(
                    str(PLANTS_PRICES[slot.name]), Vector2(0, 0)
                )
            )
            container.add_child(inner_container)
            logging.info(slot)

    def on_wave_started(
        self,
        _event: EventFlow,
        wave_number: int,
    ):
        self.wave_number.get(TextRenderComponent).set_text(
            f"Текущая волна: {wave_number}"
        )

    def update(self, delta_time):
        self.time_before_wave.get(TextRenderComponent).set_text(
            f"Следующая волна через: {self.get_time_before_wave()}"
        )

    def show_tooltip(self, _event: EventFlow, text: str, cursor_local_pos):
        if not self.tooltip:
            tooltip_message = self.ui_factory.create_tooltip_message(
                cursor_local_pos,
                Vector2(250, 120),
                TOOLTIP_TEXT_FONT_SIZE,
                text
            )
            self.tooltip = tooltip_message

    def hide_tooltip(self, _event: EventFlow, text: str):
        if self.tooltip:
            self.tooltip.free()
            self.tooltip = None