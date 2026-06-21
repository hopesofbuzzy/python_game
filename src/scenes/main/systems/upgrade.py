import logging
from typing import Callable

from pygame.math import Vector2

# Константы
from src.config.plants import PLANTS_UPGRADE_DESCRIPTIONS
from src.core.objects import (
    Map,
    MapModelComponent,
)
from src.core.singletones.event_bus import EventBus, EventFlow
from src.factories.bullet_factory import BulletFactory
from src.factories.dialog_builder import DialogBuilder
from src.factories.plant_factory import PlantFactory
from src.factories.ui_factory import UIFactory
from src.scenes.main.objects import (
    BasePlant,
    DataComponent,
    MapLevelDataComponent,
    UpgradeComponent,
)
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent
from src.scenes.main.systems.currency import CurrencyManager

UPGRADE_DIALOG_SIZE = Vector2(300, 150)
UPGRADE_BUTTON_TEXT = "Улучшить"
UPGRADE_BUTTON_FONT_SIZE = 18


class UpgradeManager:
    """Менеджер улучшений растений."""

    def __init__(
        self,
        gamemap: Map,
        currency: CurrencyManager,
        ui_factory: UIFactory,
        plant_factory: PlantFactory,
        add_object_func: Callable,
        event_bus: EventBus
    ):
        self.gamemap = gamemap
        self.currency = currency
        self.ui_factory = ui_factory
        self.plant_factory = plant_factory
        self.add_object = add_object_func
        self.upgrade_dialogs = list()
        event_bus.subscribe(
            "on_requested_upgrade_dialog",
            self.open_upgrade_dialog
        )
        event_bus.subscribe(
            "on_requested_upgrade",
            self.plant_upgrade
        )
        event_bus.subscribe(
            "on_plant_level_uped",
            self.plant_level_up
        )
        self.event_bus = event_bus

    def plant_level_up(
            self,
            _event: EventFlow,
            plant: BasePlant,
            target_plant_name
    ):
        """Трансформация растения после уровня улучшения."""
        self.close_all_upgrade_dialogs()
        tile_pos = plant.get(DataComponent).tile_pos
        global_pos_centred = (
            self.gamemap
            .get(MapModelComponent)
            .tile_to_pos_centred(Vector2(tile_pos))
        )
        logging.debug(f"Начинаем улучшение до {target_plant_name}")
        new_plant = self.plant_factory.create_plant(
            target_plant_name,
            global_pos_centred,
            tile_pos
        )
        self.gamemap.get(MapLevelDataComponent).remove_plant(
            tile_pos
        )
        self.gamemap.get(MapLevelDataComponent).add_plant(
            tuple(new_plant.get(DataComponent).tile_pos)
        )
        plant.free()
        # Открытие нового окна улучшения.
        self.open_upgrade_dialog(
            EventFlow(),
            new_plant
        )

    def plant_upgrade(self, _event: EventFlow, plant: BasePlant):
        """Одноразовое улучшение растения."""
        price = plant.get(UpgradeComponent).get_upgrade_cost()
        if self.currency.suns >= price:
            self.currency.decrease_suns(price)
            plant.get(UpgradeComponent).upgrade()
            logging.debug(f"Растение улучшено")

    def open_upgrade_dialog(
        self,
        _event: EventFlow,
        plant: BasePlant
    ):
        """Открытие диалогового окна улучшения растения."""
        self.close_all_upgrade_dialogs()
        plant_name = plant.get(DataComponent).name
        dialog = (
            DialogBuilder(
                self.add_object,
                self.ui_factory,
                self.event_bus
            )
            .with_dialog(
                Vector2(0, 0),
                UPGRADE_DIALOG_SIZE,
                plant
            )
            .with_text(PLANTS_UPGRADE_DESCRIPTIONS[plant_name], 18)
            .with_button(
                UPGRADE_BUTTON_TEXT,
                UPGRADE_BUTTON_FONT_SIZE,
                plant
            )
            .build()
        )
        self.upgrade_dialogs.append(dialog)

    def close_all_upgrade_dialogs(self):
        """Закрытие всех диалоговых окон улучшения растений."""
        for dialog in self.upgrade_dialogs:
            dialog.free()
        self.upgrade_dialogs.clear()