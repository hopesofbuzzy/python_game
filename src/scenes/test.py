from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.systems.entity_factory import EntityFactory
from src.core.objects import *
from src.objects import *

class TestScene(Scene):
    LEVEL_PATH = "res/levels/2.csv"
    TILESET_PATH = "res/tileset.png"
    plants = 0

    def ready(self):
        tilemap = self.entity_factory.create_tilemap(
            position=Vector2(0, 0),
            tiles_path=self.LEVEL_PATH,
            tileset_path=self.TILESET_PATH
        )
        self.cursor.on_left_click.subscribe(tilemap.controller.on_left_click)
        tilemap.controller.on_tile_click.subscribe(self.on_tile_click)

        # player_model = PlayerModel(
        #     position=Vector2(100, 300),
        #     velocity=Vector2(100, 0),
        #     speed=150,
        #     shape=RectShape(size=self.PLAYER_SIZE) #  CircleShape(radius=12, position=Vector2(12, 12))
        # )
        # player = GameObject(
        #     model=player_model,
        #     view=SpriteView(
        #         image=self.image_loader.load_image("res/test.png"),
        #         size=self.PLAYER_SIZE
        #     ),
        #     controller=PlayerController(player_model)
        # )
        # self.add_object("player", player)

        path = PathModel(
            local_position=Vector2(0, 0),
            points=[
                [950, 150],
                [950, 450],
                [900, 450],
                [900, 550],
                [750, 550],
                [750, 150],
                [400, 150],
                [400, 250],
                [450, 250],
                [450, 400],
                [400, 400],
                [400, 500],
                [250, 500],
                [250, 350],
                [50, 350]
            ]
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
        # self.camera.target = player_model

    def on_tile_click(self, clicked_tile: Vector2, global_pos: Vector2):
        print(global_pos)
        plant = self.entity_factory.create_plant(
            position=global_pos
        )
        plant.model.on_bullet_spawn.subscribe(self.entity_factory.create_bullet)
        self.plants += 1
