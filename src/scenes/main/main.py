import logging

from pygame.math import Vector2

from src.core.objects import GameObject
from src.core.objects.path import PathModel
from src.core.systems.scene import Scene
from src.scenes.main.objects import (
    Inventory,
    ShooterModel,
    SunflowerModel,
)
from src.scenes.main.entity_factory import EntityFactory
from src.scenes.main.level_builder import Level, LevelBuilder
from src.scenes.main.wave_manager import WaveManager
from src.scenes.main.game_map import GameMap

START_SUNS = 150


class MainScene(Scene):
    def ready(self):
        # Фабрика объектов.
        self.entity_factory: EntityFactory = EntityFactory(
            self.add_object,
            self.il,
            self.cursor
        )
        # Строитель уровней.
        self.level_builder: LevelBuilder = LevelBuilder(
            self.add_object,
            self.il,
            self.cursor
        )
        # Уровень и карта.
        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.gamemap: GameMap = self.level.gamemap
        self.gamemap.controller.on_tile_click.subscribe(self.plant)
        # Статистика уровня.
        self.suns: int = START_SUNS
        self.inventory: Inventory = self.entity_factory.create_inventory()
        # Путь
        self.path = self.level.path
        path = PathModel(
            local_position=Vector2(0, 0),
            points=list(
                map(
                    self.gamemap.model.tile_to_pos_centred,
                    list(map(Vector2, self.path))
                )
            ),
        )
        # Оркестратор волн и спавна врагов.
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.entity_factory.create_enemy,
            path
        )
        self.wave_manager.on_enemy_reach_end.subscribe(self.game_over)

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def plant(self, tile_pos: Vector2, tile_type: int, global_pos: Vector2):
        slot = self.inventory.model.get_active_slot()
        # Условия посадки.
        if (
            slot.model.price <= self.suns
            and self.gamemap.model.is_position_free(tuple(tile_pos))
        ):
            if (
                self.gamemap.model.is_position_to_place_plant(tuple(tile_pos))
                or self.gamemap.model.is_position_to_place_road_plant(tuple(tile_pos))
            ):
                self.suns -= slot.model.price
                plant = self.entity_factory.create_plant(
                    global_pos, slot.model, slot.view
                )
                if isinstance(plant.model, SunflowerModel):
                    plant.model.on_given_sun.subscribe(self.give_sun)
                elif isinstance(plant.model, ShooterModel):
                    plant.model.on_bullet_spawn.subscribe(
                        self.entity_factory.create_bullet
                    )
                self.gamemap.controller.add_plant(plant, tuple(tile_pos))

    def give_sun(self, suns: int):
        self.suns += suns
        logging.info(f"Солнышки: {self.suns}")

    def game_over(self):
        self.exit()