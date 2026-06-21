from pygame.math import Vector2

from src.core.objects.components.collision import MovementComponent
from src.core.objects.components.position import PositionComponent
from src.core.objects.event import Event


class PathComponent:
    def __init__(self, points: list):
        self.points = [Vector2(p) for p in points][::-1]


class PatrolComponent:
    """Модель компонента следования по пути."""

    def __init__(self, _entity, path: PathComponent, point_radius: int = 3):
        self.entity = _entity
        self.path = path
        self.point_radius = point_radius
        self._target_point_ref = len(self.path.points) - 1
        self.on_start_patrol: Event = Event()
        self.start_patrol()

    def start_patrol(self):
        """Старт патрулирования."""
        self.on_start_patrol.emit(self.path.points[self._target_point_ref])
        self.entity.get(PositionComponent).position = self.path.points[
            self._target_point_ref
        ]

    def bind(self, build_context):
        self.end_patrol_func = build_context.end_patrol_func

    def update(self, delta_time):
        self.follow_path()

    def follow_path(self):
        """Следование по пути."""
        if self._target_point_ref >= 0:
            # Выбор целевой позиции.
            target_point = self.path.points[self._target_point_ref]
            dx = target_point.x - self.entity.get(PositionComponent).position.x
            dy = target_point.y - self.entity.get(PositionComponent).position.y
            dist = dx**2 + dy**2
            min_dist = (self.point_radius) ** 2
            if dist <= min_dist:
                self.choose_next_point()
            else:
                d = Vector2(dx, dy).normalize()
                self.entity.get(MovementComponent).set_velocity(d[0], d[1])
        elif self._target_point_ref == -1:
            self.choose_next_point()
        else:
            self.end_patrol_func()
            self.entity.get(MovementComponent).set_velocity(0, 0)

    def choose_next_point(self) -> int | None:
        """Выбирает следующую целевую точку пути."""
        self._target_point_ref -= 1
        return self._target_point_ref
