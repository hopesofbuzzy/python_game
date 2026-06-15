import logging

from pygame.math import Vector2

from src.core.objects import GameObject
from src.core.objects.path import PathModel
from src.core.systems.scene import Scene
from src.scenes.main.factories.enemy_factory import EnemyFactory
from src.scenes.main.factories.bullet_factory import BulletFactory
from src.scenes.main.factories.inventory_factory import InventoryFactory
from src.scenes.main.factories.path_factory import PathFactory
from src.scenes.main.builders.plant_builder import PlantBuilder
from src.scenes.main.game_map import GameMap
from src.scenes.main.level_builder import Level, LevelBuilder
from src.scenes.main.objects import (
    Inventory,
    ShooterModel,
    SunflowerModel,
)
from src.scenes.main.wave_manager import WaveManager

START_SUNS = 150


class MainScene(Scene):
    def ready(self):
        # Статистика уровня.
        self.suns: int = START_SUNS
        # Загрузка уровня.
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object,
            self.il,
            self.cursor
        )
        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.gamemap: GameMap = self.level.gamemap
        self.gamemap.controller.on_tile_click.subscribe(self.plant)
        # Фабрики объектов.
        self.enemy_factory: EnemyFactory = EnemyFactory(
            self.add_object,
            self.il
        )
        self.bullet_factory: BulletFactory = BulletFactory(
            self.add_object,
            self.il
        )
        self.inventory_factory: InventoryFactory = InventoryFactory(
            self.add_object,
            self.il,
            self.cursor
        )
        self.inventory: Inventory = self.inventory_factory.create_inventory()
        self.path_factory: PathFactory = PathFactory()
        # Путь
        path = self.path_factory.create_path(
            self.level.path,
            self.gamemap.model.tile_to_pos_centred
        )
        # Оркестратор волн и спавна врагов.
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.enemy_factory.create_enemy,
            path
        )
        self.wave_manager.on_enemy_reach_end.subscribe(self.game_over)

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def plant(self, tile_pos: Vector2, tile_type: int, global_pos: Vector2):
        """Посадка растения."""
        slot = self.inventory.model.get_active_slot()
        # Условия посадки.
        if (
            slot
            and slot.model.price <= self.suns
            and self.gamemap.model.is_position_free(tuple(tile_pos))
        ):
            if (
                self.gamemap.model.is_position_to_place_plant(tuple(tile_pos))
                or self.gamemap.model.is_position_to_place_road_plant(tuple(tile_pos))
            ):
                self.suns -= slot.model.price
                # Создание растения.
                plant = (PlantBuilder(self.add_object, self.il, self.cursor)
                    .with_plant(
                        global_pos, tuple(tile_pos), slot.model, slot.view
                    )
                    .with_button()
                    .build()
                )
                # События
                plant.controller.on_dialog_requested.subscribe(self.create_dialog)
                if isinstance(plant.model, SunflowerModel):
                    plant.model.on_given_sun.subscribe(self.give_sun)
                    plant.model.on_death.subscribe(self.gamemap.model.remove_plant)
                elif isinstance(plant.model, ShooterModel):
                    plant.model.on_bullet_spawn.subscribe(
                        self.bullet_factory.create_bullet
                    )
                self.gamemap.controller.add_plant(plant, tuple(tile_pos))
                

    def give_sun(self, suns: int):
        """Выдача солыншек."""
        self.suns += suns
        logging.info(f"Солнышки: {self.suns}")

    def create_dialog(self, plant_model):
        logging.debug("Появляется диалог")

    def game_over(self):
        """Проигрыш."""
        self.exit()