from pygame.math import Vector2

from src.core.objects.game_object import Model

class KinematicBodyModel(Model):
    def __init__(self):
        super().__init__()
        self.velocity: Vector2 = Vector2(0, 0)