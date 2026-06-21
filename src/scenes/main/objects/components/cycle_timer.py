from src.core.objects.components.component_registry import ComponentRegistry


@ComponentRegistry.register("cycle_timer")
class CycleTimerComponent:
    """Циклический таймер, выдающий данные по циклу."""

    def __init__(self, _entity, time, data):
        self.time = time
        self.data = data
        self._timer = time

    def bind(self, build_context):
        self.timeout_func = build_context.timeout_func

    def update(self, delta_time):
        self._timer -= delta_time
        if self._timer <= 0.0:
            self.timeout_func(self.data)
            self._timer = self.time
