from typing import Callable
import logging
from pygame.math import Vector2

from src.core.objects import TextRenderComponent, ClickHandlerComponent
from src.core.objects.event import Event
from src.core.singletones.event_bus import EventBus, EventFlow
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.objects.components.inventory import Slot
from src.scenes.main.systems.currency import CurrencyManager
from src.config.plants import PLANTS_PRICES

SUNS_TEXT_POSITION = Vector2(0, 0)
SUNS_TEXT_SIZE = 25
WAVE_NUMBER_TEXT_POSITION = SUNS_TEXT_POSITION + Vector2(0, 20)
WAVE_NUMBER_TEXT_SIZE = 25
TIME_BEFORE_WAVE_TEXT_POSITION = WAVE_NUMBER_TEXT_POSITION + Vector2(0, 30)
TIME_BEFORE_WAVE_TEXT_SIZE = 15
INVENTORY_POSITION = TIME_BEFORE_WAVE_TEXT_POSITION + Vector2(0, 300)
INVENTORY_SIZE = Vector2(60, 300)
INVENTORY_COLOR = (150, 150, 150)
SLOT_SIZE = Vector2(60, 65)
SLOT_COLOR = (100, 100, 100)

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

    def build_inventory(self, inventory_slots: list[Slot]):
        container = self.ui_factory.create_vertical_container(
            INVENTORY_POSITION, INVENTORY_SIZE, None, INVENTORY_COLOR, 5
        )
        for slot in inventory_slots:
            inner_container = self.ui_factory.create_vertical_container(
                Vector2(0, 0), SLOT_SIZE, None, SLOT_COLOR, -5
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
            inner_container.add_child(image)
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