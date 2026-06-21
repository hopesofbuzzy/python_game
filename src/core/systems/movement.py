from src.core.objects import *
from src.core.objects.components.collision import MovementComponent
from src.core.objects.scene import Scene


class MovementSystem:
    """
    Система движения тел кинематики
    (без сложной физики, только скорость и ускорение).
    """

    def update(self, scene: Scene, delta_time: float):
        """
            Осуществляет движение всех
            объектов с соотв. компонентом на сцене.
        """
        for object in scene.object_registry.values():
            if object.has(MovementComponent, PositionComponent):
                object.get(PositionComponent).position += (
                    object.get(MovementComponent).velocity * delta_time
                )
