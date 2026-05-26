from src.core.systems.scene import Scene
from src.core.objects import *

class MovementSystem:
    """
        Система движения тел кинематики
        (без сложной физики, только скорость и ускорение).
    """
    def update(self, scene: Scene, delta_time: float):
        print("КАДР")
        for object in scene.object_registry.values():
            model = object.model
            
            if isinstance(model, KinematicBodyModel) or isinstance(model, AreaModel):
                
                model.position += model.velocity * delta_time
                print(model.velocity, f"{model.position - model.velocity * delta_time} -> {model.position}")