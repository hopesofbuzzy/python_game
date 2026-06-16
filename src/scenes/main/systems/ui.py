from pygame.math import Vector2

from src.core.objects import TextRenderComponent
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.systems.currency import CurrencyManager

SUNS_TEXT_POSITION = Vector2(0, 0)
SUNS_TEXT_SIZE = 20

class UIManager:
    """Менеджер интерфейса игры (HUD)"""
    def __init__(
        self,
        ui_factory: UIFactory,
        currency: CurrencyManager
    ):
        self.ui_factory = ui_factory
        self.currency = currency
        self.build_interface()
        
    def build_interface(self):
        self.suns_text = self.ui_factory.create_text(
            f"Солнышки: {self.currency.suns}",
            SUNS_TEXT_POSITION,
            SUNS_TEXT_SIZE
        )
        self.currency.on_suns_update.subscribe(
            lambda s: self.suns_text.get(TextRenderComponent).set_text(f"Солнышки: {s}")
        )