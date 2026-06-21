from src.core.objects.game_object import GameObject


class Bullet(GameObject):
    """Пуля."""
    def update(self, delta_time: float):
        return super().update(delta_time)
