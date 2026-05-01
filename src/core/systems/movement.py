from src.core.systems.scene import Scene
from src.core.objects import *

class MovementSystem:
    """
        Система движения тел кинематики
        (без сложной физики, только скорость и ускорение).
    """
    def update(self, scene: Scene, delta_time: float):
        for object in scene.object_registry.values():
            model = object.model
            if type(model) is KinematicBodyModel:
                # print(model.position, model.size, model.velocity, delta_time)
                model.position += model.velocity * delta_time