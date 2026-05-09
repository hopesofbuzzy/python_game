from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.objects import *
from src.objects import *

class TestScene(Scene):
    PLAYER_SIZE = Vector2(40, 40)
    ENEMY_SIZE = Vector2(40, 40)

    def ready(self):
        player_model = PlayerModel(
            position=Vector2(100, 300),
            velocity=Vector2(100, 0),
            speed=150,
            shape=RectShape(size=self.PLAYER_SIZE) #  CircleShape(radius=12, position=Vector2(12, 12))
        )
        player = GameObject(
            model=player_model,
            view=SpriteView(
                image=self.image_loader.load_image("res/test.png"),
                size=self.PLAYER_SIZE
            ),
            controller=PlayerController(player_model)
        )
        self.add_object("player", player)

        enemy_model = EnemyModel(
            position=Vector2(200, 300),
            velocity=Vector2(0, 0),
            shape=RectShape(size=self.ENEMY_SIZE)  #CircleShape(radius=12, position=Vector2(12, 12)) 
        )
        enemy = GameObject(
            model=enemy_model,
            view=RectView(color=(255, 25, 25), size=self.ENEMY_SIZE),
            controller=Controller(enemy_model)
        )
        self.add_object("enemy_1", enemy)

        enemy_model2 = EnemyModel(
            position=Vector2(250, 320),
            velocity=Vector2(0, 0),
            shape=RectShape(size=self.ENEMY_SIZE)  #CircleShape(radius=12, position=Vector2(12, 12)) 
        )
        enemy2 = GameObject(
            model=enemy_model2,
            view=RectView(color=(25, 25, 255), size=self.ENEMY_SIZE),
            controller=Controller(enemy_model)
        )
        self.add_object("enemy_2", enemy2)