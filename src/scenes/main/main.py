import logging

from pygame.math import Vector2
from src.scenes.main.level.level_builder import Level, LevelBuilder

# Компоненты.
from src.core.objects.components.map import Map, MapControllerComponent, MapModelComponent
from src.core.objects.components.targeting import TargetingComponent
from src.core.resources.image_loader import image_loader
from src.core.systems.input import cursor

# Составляющие сцены.
from src.core.objects.scene import Scene
from src.scenes.main.objects.components.cycle_timer import CycleTimerComponent
from src.scenes.main.objects.components.health import HealthComponent
from src.scenes.main.factories.bullet_factory import BulletFactory

# Фабрики.
from src.scenes.main.factories.enemy_factory import EnemyFactory
from src.scenes.main.factories.inventory_factory import InventoryFactory
from src.scenes.main.factories.path_factory import PathFactory
from src.scenes.main.factories.plant_factory import PlantFactory
from src.scenes.main.objects import Inventory, InventoryModelComponent
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent

# Константы
from src.scenes.main.objects.plants import PLANTS, PLANTS_PRICES
from src.scenes.main.wave_manager import WaveManager

START_SUNS = 150


class MainScene(Scene):
    def ready(self):
        # Статистика уровня.
        self.suns: int = START_SUNS
        # Загрузка уровня.
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object,
        )
        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.gamemap: Map = self.level.map
        self.gamemap.get(MapControllerComponent).on_tile_click.subscribe(self.plant)
        # Фабрики объектов.
        self.enemy_factory: EnemyFactory = EnemyFactory(self.add_object )
        self.bullet_factory: BulletFactory = BulletFactory(self.add_object,)
        self.plant_factory = PlantFactory(self.add_object)
        self.inventory_factory: InventoryFactory = InventoryFactory(self.add_object)
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        self.path_factory: PathFactory = PathFactory()
        # Путь
        path = self.path_factory.create_path_component(
            self.level.path,
            self.gamemap.get(MapModelComponent).tile_to_pos_centred
        )
        # Оркестратор волн и спавна врагов.
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.enemy_factory.create_enemy,
            path
        )
        self.wave_manager.on_enemy_reached_end.subscribe(self.game_over)

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def plant(
            self,
            tile_pos: Vector2,
            global_pos_centred: Vector2,
            tile_type: int,
            global_pos: Vector2
        ):
        """Посадка растения."""
        slot = self.inventory.get(InventoryModelComponent).get_active_slot()
        map_level_data = self.gamemap.get(MapLevelDataComponent)
        # Условия посадки.
        if (
            slot
            and self.check_suns(slot)
            and map_level_data.is_position_free(tuple(tile_pos))
        ):
            if (
                map_level_data.is_position_to_place_plant(tuple(tile_pos))
                or map_level_data.is_position_to_place_road_plant(tuple(tile_pos))
            ):
                self.suns -= self.get_plant_price(slot)
                # Создание растения.
                plant = self.plant_factory.create_plant(
                    slot,
                    global_pos_centred,
                    tile_pos
                )
                # События
                # plant.controller.on_dialog_requested.subscribe(self.create_dialog)
                if plant.has(HealthComponent):
                    plant.get(HealthComponent).on_death.subscribe(
                        self.gamemap.get(MapLevelDataComponent).remove_plant
                    )
                if plant.has(CycleTimerComponent):
                    plant.get(CycleTimerComponent).on_timeout.subscribe(self.give_sun)
                if plant.has(TargetingComponent):
                    plant.get(TargetingComponent).on_shoot.subscribe(
                        self.bullet_factory.create_bullet
                    )
                self.gamemap.get(MapLevelDataComponent).add_plant(
                    plant,
                    tuple(tile_pos)
                )

    def check_suns(self, plant: str) -> bool:
        return self.suns >= PLANTS_PRICES[plant]

    def get_plant_price(self, plant: str) -> int:
        return PLANTS_PRICES[plant]

    def give_sun(self, suns: int):
        """Выдача солыншек."""
        self.suns += suns
        logging.info(f"Солнышки: {self.suns}")

    def create_dialog(self, plant_model):
        logging.debug("Появляется диалог")

    def game_over(self):
        """Проигрыш."""
        self.exit()