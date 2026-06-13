from src.objects import EnemyModel, ShooterModel


class TargetingSystem:
    """Система обнаружения целей для стрельбы."""

    def __init__(self, uniform_grod):
        self.uniform_grid = uniform_grod

    def update(self, scene, delta_time: float):
        """Проверка соседей башни для стрельбы."""
        for object in scene.object_registry.values():
            if isinstance(object.model, ShooterModel):
                others = self.uniform_grid.query_circle(object, object.model.range)
                enemies = [
                    other.model
                    for other in others
                    if isinstance(other.model, EnemyModel) and object.uid >= other.uid
                ]
                if enemies:
                    object.model.handle_targets(enemies, delta_time)
