from src.core.objects.event import Event
from src.core.objects.game_object import GameObject


class CycleTimerComponent:
    """Циклический таймер, выдающий данные по циклу."""
    def __init__(self, time, data):
        self.time = time
        self.data = data
        self._timer = time
        self.on_timeout: Event = Event()

    def update(self, delta_time):
        self._timer -= delta_time
        if self._timer <= 0.0:
            self.on_timeout.emit(self.data)
            self._timer = self.time
