import logging

from pygame.math import Vector2

from src.core.objects import (
    Map,
    MapControllerComponent,
    MapModelComponent,
    MapViewComponent,
)
from src.core.objects.scene import Scene
from src.core.singletones.event_bus import EventFlow
from src.factories.bullet_factory import BulletFactory
from src.factories.cursor_circle_factory import CursorCircleFactory

# Фабрики и строители.
from src.factories.enemy_factory import EnemyFactory
from src.factories.inventory_factory import InventoryFactory
from src.factories.path_factory import PathFactory
from src.factories.plant_factory import PlantFactory
from src.factories.ui_factory import UIFactory
from src.scenes.main.objects import (
    Inventory,
    InventoryModelComponent,
)
from src.scenes.main.objects.components.map_level_data import (
    MapLevelDataComponent,
)
from src.scenes.main.systems.bullet import BulletController

# Системы текущей сцены.
from src.scenes.main.systems.currency import CurrencyManager
from src.scenes.main.systems.enemy import EnemyController
from src.scenes.main.systems.inventory import InventoryManager
from src.scenes.main.systems.level import LevelManager
from src.scenes.main.systems.music import MusicManager
from src.scenes.main.systems.plant import PlantController
from src.scenes.main.systems.ui import UIManager
from src.scenes.main.systems.upgrade import UpgradeManager
from src.scenes.main.systems.waves import WaveManager
from src.scenes.win.win import WinScene
from src.scenes.lose.lose import LoseScene


class MainScene(Scene):
    def ready(self):
        self.setup_factories()
        self.setup_level()
        self.setup_systems()
        self.setup_controllers()
        self.setup_waves()
        self.setup_ui()
        self.event_bus.subscribe("on_enemy_reached_end", self.game_over)
        self.event_bus.subscribe("on_win", self.win)

    def setup_factories(self):
        """Настраивает мелкие фабрики."""
        self.inventory_factory: InventoryFactory = InventoryFactory(
            self.add_object, self.event_bus
        )
        self.path_factory: PathFactory = PathFactory()
        self.ui_factory: UIFactory = UIFactory(self.add_object, self.event_bus)
        self.cursor_circle_factory = CursorCircleFactory(self.add_object)

    def setup_level(self):
        """Генерирует и собирает уровень."""
        self.level = LevelManager(self.add_object).generate_level()
        self.gamemap: Map = self.level.map
        self.gamemap.get(MapControllerComponent).on_tile_click.subscribe(
            self.handle_map_click
        )

    def setup_systems(self):
        """Настраивает системы."""
        self.music_manager: MusicManager = MusicManager(
            self.audio_loader, self.event_bus
        )
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        self.inventory_manager: InventoryManager = InventoryManager(
            self.inventory,
            self.cursor_circle_factory,
            self.gamemap.get(MapViewComponent).tile_size,
            self.event_bus,
        )
        self.currency = CurrencyManager(self.event_bus)

    def setup_controllers(self):
        """
        Настраивает системы, связанные с контролем
        спавна сущностей (EventBus driven).
        """
        self.bullet_factory: BulletFactory = BulletFactory(
            self.add_object, self.event_bus
        )
        self.bullet_controller = BulletController(self.event_bus)
        self.enemy_factory: EnemyFactory = EnemyFactory(
            self.add_object, self.ui_factory, self.event_bus
        )
        self.enemy_controller = EnemyController(
            self.enemy_factory, self.event_bus
        )
        self.plant_factory: PlantFactory = PlantFactory(
            self.add_object,
            self.bullet_factory,
            self.ui_factory,
            self.event_bus,
        )
        self.plant_controller = PlantController(
            self.currency,
            self.inventory.get(InventoryModelComponent),
            self.gamemap.get(MapLevelDataComponent),
            self.event_bus,
            self.plant_factory,
        )
        self.upgrade: UpgradeManager = UpgradeManager(
            self.gamemap,
            self.currency,
            self.ui_factory,
            self.plant_factory,
            self.add_object,
            self.event_bus,
        )

    def setup_ui(self):
        """Настраивает интерфейс."""
        self.ui_manager: UIManager = UIManager(
            self.ui_factory,
            self.currency,
            self.event_bus,
            self.wave_manager.get_time_before_wave,
            self.inventory.get(InventoryModelComponent).get_slots(),
        )

    def setup_waves(self):
        """Настраивает волны."""
        path = self.path_factory.create_path_component(
            self.level.path,
            self.gamemap.get(MapModelComponent).tile_to_pos_centred,
        )
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.enemy_factory.create_enemy,
            path,
            self.event_bus,
        )

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        self.ui_manager.update(delta_time)
        return super().update(delta_time)

    def handle_map_click(
        self,
        event: EventFlow,
        tile_pos: Vector2,
        global_pos_centred: Vector2,
        tile_type: int,
        global_pos: Vector2,
    ):
        """Соединяет клик на тайл с контроллерами."""
        self.upgrade.close_all_upgrade_dialogs()
        self.plant_controller.try_plant(event, tile_pos, global_pos_centred)

    def win(self, _event: EventFlow):
        """Победа."""
        self.global_data["waves"] = self.wave_manager.get_wave_count()
        self.global_data["suns"] = self.currency.get_suns()
        self.global_data["enemies_destroyed"] = (
            self.enemy_controller.get_enemies_destroyed_count()
        )
        self.change_scene(WinScene)

    def game_over(self, _event: EventFlow):
        """Проигрыш."""
        self.global_data["waves"] = self.wave_manager.get_wave_count()
        self.global_data["suns"] = self.currency.get_suns()
        self.global_data["enemies_destroyed"] = (
            self.enemy_controller.get_enemies_destroyed_count()
        )
        self.change_scene(LoseScene)
