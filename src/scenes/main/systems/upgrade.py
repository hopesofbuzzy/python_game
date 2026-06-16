import logging
from pygame.math import Vector2
from typing import Callable

from src.core.singletones.event_bus import EventFlow, EventBus

from src.scenes.main.factories.dialog_builder import DialogBuilder
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.bullet_factory import BulletFactory
from src.scenes.main.factories.ui_factory import UIFactory

from src.scenes.main.objects import (
    BasePlant,
    UpgradeComponent,
    MapLevelDataComponent,
    PlantDataComponent
)
from src.core.objects import (
    Map,
    MapModelComponent,
)
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent

from src.scenes.main.systems.currency import CurrencyManager

# Константы
from src.scenes.main.objects.plants import PLANTS_DESCRIPTIONS

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
        bullet_factory: BulletFactory,
        add_object_func: Callable
    ):
        self.gamemap = gamemap
        self.currency = currency
        self.ui_factory = ui_factory
        self.bullet_factory = bullet_factory
        self.add_object = add_object_func
        self.upgrade_dialogs = list()

    def plant_level_up(
            self,
            _event: EventFlow,
            plant: BasePlant,
            target_plant_name
    ):
        """Трансформация растения после уровня улучшения."""
        self.close_all_upgrade_dialogs()
        global_pos_centred = (
            self.gamemap
            .get(MapModelComponent)
            .tile_to_pos_centred(Vector2(plant.tile_pos))
        )
        logging.debug(f"Начинаем улучшение до {target_plant_name}")
        new_plant = (
            PlantBuilder(
                self.add_object,
                self.bullet_factory,
                self.currency.give_sun,
                self.gamemap.get(MapLevelDataComponent).remove_plant,
                self.ui_factory
            )
            .with_replace(plant.tile_pos)
            .with_plant(target_plant_name, global_pos_centred, plant.tile_pos)
            .with_upgrade()
            .with_button()
            .build()
        )
        self.gamemap.get(MapLevelDataComponent).add_plant(
            tuple(new_plant.tile_pos)
        )
        self.gamemap.get(MapLevelDataComponent).remove_plant(
            plant.tile_pos
        )
        plant.free()
        # Открытие нового окна улучшения.
        next_request_upgrade_func = new_plant.get(UpgradeComponent).request_upgrade
        self.open_upgrade_dialog(
            EventFlow(),
            new_plant,
            next_request_upgrade_func
        )

    def open_upgrade_dialog(
            self,
            _event: EventFlow,
            plant: BasePlant,
            request_upgrade_func
    ):
        """Открытие диалогового окна улучшения растения."""
        self.close_all_upgrade_dialogs()
        plant_name = plant.get(PlantDataComponent).name
        dialog = (
            DialogBuilder(
                self.add_object,
                self.ui_factory
            )
            .with_dialog(
                Vector2(0, 0),
                UPGRADE_DIALOG_SIZE,
                plant
            )
            .with_text(PLANTS_DESCRIPTIONS[plant_name], 18)
            .with_button(
                UPGRADE_BUTTON_TEXT,
                UPGRADE_BUTTON_FONT_SIZE,
                request_upgrade_func
            )
            .build()
        )
        self.upgrade_dialogs.append(dialog)

    def close_all_upgrade_dialogs(self):
        """Закрытие всех диалоговых окон улучшения растений."""
        for dialog in self.upgrade_dialogs:
            dialog.free()
        self.upgrade_dialogs.clear()

    def plant_upgrade(
            self,
            _event: EventFlow,
            plant: BasePlant,
            price: int,
            upgrade_func
    ):
        """Одноразовое улучшение растения."""
        if self.currency.suns >= price:
            self.currency.decrease_suns(price)
            upgrade_func()
            logging.debug(f"Растение улучшено")