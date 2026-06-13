import logging

from pygame.math import Vector2

from src.core.objects import GameObject
from src.core.objects.path import PathModel
from src.tools.level_builder import Level, ParsedMap, LevelBuilder
from src.tools.entity_factory import EntityFactory
from src.tools.wave_manager import WaveManager
from src.core.systems.scene import Scene
from src.objects import (
    EnemyModel,
    EnemyView,
    FastEnemyModel,
    FastEnemyView,
    Inventory,
    InventoryModel,
    MushroomModel,
    MushroomView,
    ShooterModel,
    SunflowerModel,
)

START_SUNS = 150


class TestScene(Scene):
    def ready(self):
        # Фабрика объектов.
        self.entity_factory: EntityFactory = EntityFactory(self, self.il, self.cursor)
        # Строитель уровней.
        self.level_builder: LevelBuilder = LevelBuilder(self, self.il, self.cursor)

        self.level: Level = self.level_builder.load_and_create_level(Vector2(0, 0), "2")
        self.plants: int = 0
        self.suns: int = START_SUNS
        self.inventory: Inventory = self.entity_factory.create_inventory()

        self.path = self.level.path
        self.parsed_map: ParsedMap = self.level.parsed_map
        self.level.tilemap.controller.on_tile_click.subscribe(self.plant)

        path = PathModel(
            local_position=Vector2(0, 0),
            points=list(
                map(
                    self.level.tilemap.model.tile_to_pos,
                    list(map(Vector2, self.path))
                )
            ),
        )
        # Оркестратор волн
        self.wave_manager: WaveManager = WaveManager(
            self.level.parsed_waves,
            self.entity_factory.create_enemy,
            path
        )

    def update(self, delta_time: float):
        self.wave_manager.update(delta_time)
        return super().update(delta_time)

    def plant(self, tile_pos: Vector2, tile_type: int, global_pos: Vector2):
        slot = self.inventory.model.slots[self.inventory.model.active_slot]
        if not slot.model.price <= self.suns:
            return
        plant_cond = (
            tuple(tile_pos) in self.parsed_map.poses_to_place
            and slot.model is not SunflowerModel
        )
        sunflower_cond = (
            tuple(tile_pos) in self.parsed_map.path_poses
            and slot.model is SunflowerModel
        )
        if plant_cond or sunflower_cond:
            self.suns -= slot.model.price
            plant = self.entity_factory.create_plant(
                global_pos, slot.model, slot.view
            )
            if isinstance(plant.model, SunflowerModel):
                plant.model.on_given_sun.subscribe(self.give_sun)
            elif isinstance(plant.model, ShooterModel):
                plant.model.on_bullet_spawn.subscribe(self.entity_factory.create_bullet)
            self.plants += 1

    def give_sun(self, suns: int):
        self.suns += suns
        logging.info(f"Солнышки: {self.suns}")