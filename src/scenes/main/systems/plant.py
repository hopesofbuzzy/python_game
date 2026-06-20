from typing import Callable, Optional

from pygame.math import Vector2

from src.core.objects import Map
from src.core.singletones.event_bus import EventFlow
from src.scenes.main.factories.bullet_factory import BulletFactory
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.objects import InventoryModelComponent, MapLevelDataComponent, BasePlant, DataComponent
from src.scenes.main.systems.currency import CurrencyManager


class PlantController:
    """Менеджер посадки растений."""

    def __init__(
        self,
        currency_manager: CurrencyManager,
        inventory_model: InventoryModelComponent,
        map_data: MapLevelDataComponent,
        add_object_func: Callable,
        bullet_factory: BulletFactory,
        ui_factory: UIFactory,
        on_plant_success_func: Optional[Callable] = None
    ):
        self.currency = currency_manager
        self.inventory = inventory_model
        self.map_data = map_data
        self.add_object = add_object_func
        self.bullet_factory = bullet_factory
        self.ui_factory = ui_factory
        self.on_plant_success = on_plant_success_func

    def try_plant(
        self,
        event: EventFlow,
        tile_pos: Vector2,
        global_pos_centred: Vector2,
    ):
        """Посадка растения."""
        tuple_tile_pos = tuple(tile_pos)
        plant_name = self.inventory.get_active_slot().name
        # Условия посадки.
        if not (
            plant_name != "None"
            and self.currency.check_suns(plant_name)
            and self.map_data.is_position_free(tuple_tile_pos)
        ):
            return
        if not self.map_data.is_position_to_place_plant(plant_name, tuple_tile_pos):
            return
        # Не забыть про вычитание валюты.
        self.currency.decrease_suns(self.currency.get_plant_price(plant_name))
        # Создание растения.
        plant = (
            PlantBuilder(
                self.add_object,
                self.bullet_factory.create_bullet,
                self.currency.give_sun,
                self.map_data.remove_plant,
                self.ui_factory
            )
            .with_plant(plant_name, global_pos_centred, tuple_tile_pos)
            .with_upgrade()
            .with_button()
            .build()
        )
        self.map_data.add_plant(tuple_tile_pos)
        # Остановка события, чтобы клик не шёл дальше после посадки.
        event.stop()
        if self.on_plant_success:
            self.on_plant_success()

    def remove_plant(self, plant: BasePlant):
        self.map_data.remove_plant(plant.get(DataComponent).tile_pos)
        plant.free()