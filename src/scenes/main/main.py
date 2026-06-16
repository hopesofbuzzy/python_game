import logging

from pygame.math import Vector2

from src.core.resources.image_loader import image_loader
from src.core.systems.input import cursor

# Составляющие сцены.
from src.core.objects.scene import Scene
from src.scenes.main.level.level_builder import Level, LevelBuilder

from src.core.objects import (
    Map,
    MapControllerComponent,
    MapModelComponent,
    Event,
    TextRenderComponent,
)
from src.scenes.main.objects import UpgradeComponent, BasePlant
# Фабрики.
from src.scenes.main.factories.enemy_factory import EnemyFactory
from src.scenes.main.factories.inventory_factory import InventoryFactory
from src.scenes.main.factories.path_factory import PathFactory
from src.scenes.main.factories.plant_builder import PlantBuilder
from src.scenes.main.factories.bullet_factory import BulletFactory
from src.scenes.main.factories.ui_factory import UIFactory
from src.scenes.main.objects import Inventory, InventoryModelComponent
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent

# Константы
from src.scenes.main.objects.plants import PLANTS, PLANTS_PRICES
from src.scenes.main.wave_manager import WaveManager

START_SUNS = 300


class MainScene(Scene):
    def ready(self):
        # Статистика уровня.
        self.suns: int = START_SUNS
        self.on_suns_update: Event = Event()
        # Загрузка уровня.
        self.setup_level()
        # Фабрики объектов.
        self.setup_factories()
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        # Оркестратор волн и спавна врагов.
        self.setup_waves()
        self.build_interface()

    def setup_factories(self):
        self.enemy_factory: EnemyFactory = EnemyFactory(self.add_object )
        self.bullet_factory: BulletFactory = BulletFactory(self.add_object,)
        self.inventory_factory: InventoryFactory = InventoryFactory(self.add_object)
        self.path_factory: PathFactory = PathFactory()
        self.ui_factory: UIFactory = UIFactory(self.add_object)

    def setup_level(self):
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object,
        )
        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.gamemap: Map = self.level.map
        self.gamemap.get(MapControllerComponent).on_tile_click.subscribe(self.plant)

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

    def build_interface(self):
        self.suns_text = self.ui_factory.create_text(f"Солнышки: {self.suns}", 20)
        self.on_suns_update.subscribe(
            lambda s: self.suns_text.get(TextRenderComponent).set_text(f"Солнышки: {s}")
        )

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
                self.decrease_suns(self.get_plant_price(slot))
                # Создание растения.
                plant = (
                    PlantBuilder(
                        self.add_object,
                        self.bullet_factory,
                        self.give_sun,
                        self.gamemap.get(MapLevelDataComponent).remove_plant,
                        self.level_up,
                        self.upgrade
                    )
                    .with_plant(
                        slot,
                        global_pos_centred,
                        tile_pos
                    )
                    .with_button()
                    .with_upgrade()
                    .build()
                )
                self.gamemap.get(MapLevelDataComponent).add_plant(
                    tuple(tile_pos)
                )

    def level_up(self, plant: BasePlant, target_plant_name):
        """Трансформация растения после уровня улучшения."""
        global_pos_centred = (
            self.gamemap
            .get(MapModelComponent)
            .tile_to_pos_centred(Vector2(plant.tile_pos))
        )
        logging.debug(f"Начинаем улучшение {target_plant_name}")
        new_plant = (
            PlantBuilder(
                self.add_object,
                self.bullet_factory,
                self.give_sun,
                self.gamemap.get(MapLevelDataComponent).remove_plant,
                self.level_up,
                self.upgrade
            )
            .with_replace(plant.tile_pos)
            .with_plant(
                target_plant_name,
                global_pos_centred,
                plant.tile_pos
            )
            .with_button()
            .with_upgrade()
            .build()
        )
        self.gamemap.get(MapLevelDataComponent).add_plant(
            tuple(new_plant.tile_pos)
        )
        self.gamemap.get(MapLevelDataComponent).remove_plant(
            plant.tile_pos
        )
        plant.free()

    def upgrade(self, plant: BasePlant):
        """Одноразовое улучшение растения."""
        upgrade_cost = plant.get(UpgradeComponent).get_upgrade_cost()
        if self.suns >= upgrade_cost:
            logging.debug(f"Растение улучшено: {self.suns}")
            self.decrease_suns(upgrade_cost)
            plant.get(UpgradeComponent).upgrade()

    def check_suns(self, plant: str) -> bool:
        return self.suns >= PLANTS_PRICES[plant]

    def get_plant_price(self, plant: str) -> int:
        return PLANTS_PRICES[plant]

    def give_sun(self, suns: int):
        """Выдача солыншек."""
        self.suns += suns
        self.on_suns_update.emit(self.suns)

    def decrease_suns(self, suns: int):
        self.suns -= suns
        self.on_suns_update.emit(self.suns)

    def create_dialog(self, plant_model):
        logging.debug("Появляется диалог")

    def game_over(self):
        """Проигрыш."""
        self.exit()