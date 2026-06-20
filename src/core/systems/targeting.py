import logging

from src.core.objects import PositionComponent
from src.core.systems.uniform_grid import UniformGrid
from src.scenes.main.objects import TargetingComponent


class TargetingSystem:
    """Система обнаружения целей для стрельбы."""

    def __init__(self, uniform_grod: UniformGrid):
        self.uniform_grid = uniform_grod

    def update(self, scene, delta_time: float):
        """Проверка соседей башни для стрельбы."""
        for object in scene.object_registry.values():
            if object.has(PositionComponent, TargetingComponent):
                others = self.uniform_grid.query_circle(
                    object,
                    object.get(TargetingComponent).range
                )
                enemies = [
                    other
                    for other in others
                    if other.has(PositionComponent) and "enemy" in other.tags
                ]
                object.get(TargetingComponent).choose_target(enemies)
