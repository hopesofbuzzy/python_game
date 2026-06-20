from typing import Callable

from pygame.math import Vector2

from src.core.objects import TextRenderComponent
from src.core.objects.event import Event
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.objects.components.inventory import Slot
from src.scenes.main.systems.currency import CurrencyManager

SUNS_TEXT_POSITION = Vector2(0, 0)
SUNS_TEXT_SIZE = 25
WAVE_NUMBER_TEXT_POSITION = SUNS_TEXT_POSITION + Vector2(0, 20)
WAVE_NUMBER_TEXT_SIZE = 25
TIME_BEFORE_WAVE_TEXT_POSITION = WAVE_NUMBER_TEXT_POSITION + Vector2(0, 30)
TIME_BEFORE_WAVE_TEXT_SIZE = 15

class UIManager:
    """Менеджер интерфейса игры (HUD)"""
    def __init__(
        self,
        ui_factory: UIFactory,
        currency: CurrencyManager,
        on_wave_started: Event,
        get_time_before_wave_func: Callable,
        inventory_slots: list[Slot]
    ):
        self.ui_factory = ui_factory
        self.currency = currency
        on_wave_started.subscribe(self.on_wave_started)
        self.get_time_before_wave = get_time_before_wave_func
        self.build_stats()
        self.build_inventory(inventory_slots)
        
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
        ...

    def on_wave_started(
        self,
        wave_number: int,
    ):
        self.wave_number.get(TextRenderComponent).set_text(
            f"Текущая волна: {wave_number}"
        )

    def update(self, delta_time):
        self.time_before_wave.get(TextRenderComponent).set_text(
            f"Следующая волна через: {self.get_time_before_wave()}"
        )