from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.objects import *
from src.objects import *

class TestScene(Scene):
    PLAYER_SIZE = Vector2(40, 40)
    ENEMY_SIZE = Vector2(40, 40)
    enemies = 0

    def ready(self):
        tilemap_model = TileMapModel(
            tiles_path="res/levels/1.csv",
            position=Vector2(0, 0),
            tileset=self.image_loader.load_image("res/tileset.png")
        )
        tilemap_controller = TileMapController(tilemap_model)
        self.cursor.on_click.subscribe(tilemap_controller.on_click)
        tilemap_controller.on_tile_click.subscribe(self.on_tile_click)
        tilemap = GameObject(
            model=tilemap_model,
            view=TileMapView(),
            controller=tilemap_controller
        )
        self.add_object("tilemap", tilemap)

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
            position=Vector2(0, 0),
            points=[
                Vector2(200, 200),
                Vector2(0, 0),
                Vector2(100, 100),
                Vector2(0, 0),
                Vector2(0, 200),
                Vector2(200, 200),
            ]
        )
        enemy_model = EnemyModel(
            position=Vector2(200, 300),
            velocity=Vector2(0, 0),
            shape=RectShape(size=self.ENEMY_SIZE),
            resolvable=False,
            path=path
        )
        enemy = GameObject(
            model=enemy_model,
            view=RectView(color=(255, 25, 25), size=self.ENEMY_SIZE),
            controller=Controller(enemy_model)
        )
        self.add_object("enemy_111", enemy)

        enemy_model = EnemyModel(
            position=Vector2(600, 300),
            velocity=Vector2(0, 0),
            shape=RectShape(size=self.ENEMY_SIZE),
            resolvable=False,
            path=path
        )
        enemy = GameObject(
            model=enemy_model,
            view=RectView(color=(255, 25, 25), size=self.ENEMY_SIZE),
            controller=Controller(enemy_model)
        )
        self.add_object("enemy_222", enemy)

        # self.camera.target = player_model

    def on_tile_click(self, clicked_tile: Vector2, global_pos: Vector2):
        enemy_model = Model(
            position=global_pos
        )
        enemy = GameObject(
            model=enemy_model,
            view=RectView(color=(255, 25, 25), size=self.ENEMY_SIZE),
            controller=Controller(enemy_model)
        )
        self.enemies += 1
        self.add_object(f"enemy_{self.enemies}", enemy)
        print(len(self.object_registry))
