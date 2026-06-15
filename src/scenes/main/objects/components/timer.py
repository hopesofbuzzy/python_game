from src.core.objects.game_object import GameObject
from src.core.objects.event import Event


class TimerComponent:
    """Одноразовый таймер"""
    def __init__(self, time):
        self.time = time
        self._timer = time
        self.on_timeout: Event = Event()

    def update(self, delta_time):
        self._timer -= delta_time
        if self._timer <= 0.0:
            self.on_timeout.emit()
