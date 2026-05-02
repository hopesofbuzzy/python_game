from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.objects import *
from src.objects.player.player import *

class TestScene(Scene):
    def ready(self):
        player_model = PlayerModel(
            position=Vector2(100, 300),
            size=Vector2(25, 25),
            velocity=Vector2(100, 0),
            speed=150
        )
        player = GameObject(
            model=player_model,
            view=RectView(color=(255, 255, 255)),
            controller=PlayerController(player_model)
        )
        self.add_object("player", player)