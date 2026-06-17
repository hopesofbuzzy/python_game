import logging

from pygame.math import Vector2

from src.core.objects import (
    Map,
    MapControllerComponent,
    MapModelComponent,
)
from src.core.objects.scene import Scene
from src.core.singletones.event_bus import EventFlow
from src.scenes.main.factories.bullet_factory import BulletFactory

# Фабрики и строители.
from src.scenes.main.factories.enemy_factory import EnemyFactory
from src.scenes.main.factories.inventory_factory import InventoryFactory
from src.scenes.main.factories.path_factory import PathFactory
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.level.builder import Level, LevelBuilder
from src.scenes.main.objects import (
    Inventory,
    InventoryModelComponent,
)
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent

# Системы текущей сцены.
from src.scenes.main.systems.currency import CurrencyManager
from src.scenes.main.systems.plant import PlantController
from src.scenes.main.systems.ui import UIManager
from src.scenes.main.systems.upgrade import UpgradeManager
from src.scenes.main.systems.waves import WaveManager

LEVEL_NAME = "2"

class MainScene(Scene):
    def ready(self):
        self.setup_factories()
        self.setup_level()
        self.setup_systems()
        self.setup_waves()
        self.event_bus.subscribe(
            "on_requested_upgrade_dialog",
            self.upgrade.open_upgrade_dialog
        )
        self.event_bus.subscribe(
            "on_requested_upgrade",
            self.upgrade.plant_upgrade
        )
        self.event_bus.subscribe(
            "on_plant_level_uped",
            self.upgrade.plant_level_up
        )

    def setup_factories(self):
        self.bullet_factory: BulletFactory = BulletFactory(self.add_object,)
        self.inventory_factory: InventoryFactory = InventoryFactory(self.add_object)
        self.path_factory: PathFactory = PathFactory()
        self.ui_factory: UIFactory = UIFactory(self.add_object)
        self.enemy_factory: EnemyFactory = EnemyFactory(
            self.add_object,
            self.ui_factory
        )

    def setup_level(self):
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object
        )
        self.level: Level = self.level_builder.load_and_create_level(
            Vector2(0, 0),
            LEVEL_NAME
        )
        self.gamemap: Map = self.level.map
        self.gamemap.get(MapControllerComponent).on_tile_click.subscribe(
            self.handle_map_click
        )

    def setup_systems(self):
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        self.currency = CurrencyManager()
        self.plant_controller = PlantController(
            self.currency,
            self.inventory.get(InventoryModelComponent),
            self.gamemap.get(MapLevelDataComponent),
            self.add_object,
            self.bullet_factory,
            self.ui_factory
        )
        self.ui_manager: UIManager = UIManager(
            self.ui_factory,
            self.currency
        )
        self.upgrade: UpgradeManager = UpgradeManager(
            self.gamemap,
            self.currency,
            self.ui_factory,
            self.bullet_factory,
            self.add_object
        )

    def setup_waves(self):
        path = self.path_factory.create_path_component(
            self.level.path,
            self.gamemap.get(MapModelComponent).tile_to_pos_centred
        )
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.enemy_factory.create_enemy,
            path
        )
        self.wave_manager.on_enemy_reached_end.subscribe(self.game_over)

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def handle_map_click(
        self,
        event: EventFlow,
        tile_pos: Vector2,
        global_pos_centred: Vector2,
        tile_type: int,
        global_pos: Vector2
    ):
        self.upgrade.close_all_upgrade_dialogs()
        self.plant_controller.try_plant(
            event, tile_pos, global_pos_centred
        )

    def game_over(self):
        """Проигрыш."""
        self.exit()