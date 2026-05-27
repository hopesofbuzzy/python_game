from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.systems.entity_factory import EntityFactory
from src.core.objects import *
from src.objects import *


class TestScene(Scene):
    plants = 0

    def ready(self):
        level = self.level_builder.load_and_create_level(
            Vector2(0, 0),
            "2"
        )
        level.tilemap.controller.on_tile_click.subscribe(self.on_tile_click)
        path = PathModel(
            local_position=Vector2(0, 0),
            points=list(map(level.tilemap.model.tile_to_pos, list(map(Vector2, level.path))))
        )
        enemy_2 = self.entity_factory.create_enemy(
            EnemyModel,
            EnemyView,
            position=Vector2(200, 200),
            path=path
        )
        enemy_1 = self.entity_factory.create_enemy(
            FastEnemyModel,
            FastEnemyView,
            position=Vector2(200, 200),
            path=path
        )
        inventory = self.entity_factory.create_inventory()
        # self.camera.target = player_model

    def on_tile_click(self, clicked_tile: Vector2, global_pos: Vector2):
        plant = self.entity_factory.create_plant(
            global_pos,
            MushroomModel,
            MushroomView
        )
        plant.model.on_bullet_spawn.subscribe(self.entity_factory.create_bullet)
        self.plants += 1
