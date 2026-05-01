from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.objects import *

class TestScene(Scene):
    def ready(self):
        rect_model = Model(position=Vector2(100, 100), size=Vector2(100, 100))
        rect = GameObject(
            model=rect_model,
            view=RectView((255, 255, 255)),
            controller=Controller(rect_model)
        )
        self.add_object("rect_1", rect)