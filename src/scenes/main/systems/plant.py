from typing import Callable, Optional

from pygame.math import Vector2

from src.core.objects import Map
from src.core.singletones.event_bus import EventBus, EventFlow
from src.factories.bullet_factory import BulletFactory
from src.factories.plant_factory import PlantFactory
from src.factories.ui_factory import UIFactory
from src.scenes.main.objects import (
    BasePlant,
    DataComponent,
    InventoryModelComponent,
    MapLevelDataComponent,
)
from src.scenes.main.systems.currency import CurrencyManager


class PlantController:
    """Менеджер посадки растений."""

    def __init__(
        self,
        currency_manager: CurrencyManager,
        inventory_model: InventoryModelComponent,
        map_data: MapLevelDataComponent,
        event_bus: EventBus,
        plant_factory: PlantFactory
    ):
        self.currency = currency_manager
        self.inventory = inventory_model
        self.map_data = map_data
        event_bus.subscribe("on_plant_death", self.remove_plant)
        self.plant_factory = plant_factory
        self.event_bus = event_bus

    def try_plant(
        self,
        event: EventFlow,
        tile_pos: Vector2,
        global_pos_centred: Vector2,
    ):
        """Посадка растения."""
        tuple_tile_pos = tuple(tile_pos)
        active_inventory_slot = self.inventory.get_active_slot()
        # Условия посадки.
        if not active_inventory_slot:
            return
        plant_name = active_inventory_slot.name
        if not self.map_data.is_position_to_place_plant(plant_name, tuple_tile_pos):
            return
        if not (
            self.currency.check_suns(plant_name)
            and self.map_data.is_position_free(tuple_tile_pos)
        ):
            return
        # Не забыть про вычитание валюты.
        self.currency.decrease_suns(self.currency.get_plant_price(plant_name))
        # Создание растения.
        plant = self.plant_factory.create_plant(
            plant_name,
            global_pos_centred,
            tuple_tile_pos
        )
        self.map_data.add_plant(tuple_tile_pos)
        self.event_bus.fire("on_inventory_zero_slot_set")
        # Остановка события, чтобы клик не шёл дальше после посадки.
        event.stop()

    def remove_plant(self,_event: EventFlow, plant: BasePlant):
        self.map_data.remove_plant(plant.get(DataComponent).tile_pos)
        plant.free()