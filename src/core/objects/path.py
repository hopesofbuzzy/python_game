import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import *
from src.core.systems.event import Event


@dataclass
class PathModel(Model):
    points: list = field(default_factory=list)

    def __post_init__(self):
        self.points = list(map(Vector2, self.points))[::-1]


@dataclass
class PathBodyModel(AreaModel):
    """Модель объекта следования по пути."""

    path: PathModel = field(
        default_factory=lambda: PathModel(local_position=Vector2(0, 0), points=list())
    )
    point_radius: int = 3
    _target_point_ref: int = -1

    on_reach_end: Event = field(default_factory=lambda: Event())

    def __post_init__(self):
        self._target_point_ref = len(self.path.points) - 1
        self.position = self.path.points[self._target_point_ref]

    def update(self, delta_time: float):
        self.follow_path()

    def follow_path(self):
        """Следует по пути."""
        if self._target_point_ref >= 0:
            target_point = self.path.points[self._target_point_ref]
            dx = target_point.x - self.position.x
            dy = target_point.y - self.position.y
            dist = dx**2 + dy**2
            min_dist = (self.point_radius) ** 2
            if dist <= min_dist:
                self.choose_next_point()
                # print(self.position, "->", target_point)
            else:
                d = Vector2(dx, dy).normalize()
                self.set_velocity(d[0], d[1])
        elif self._target_point_ref == -1:
            self.choose_next_point()
        else:
            self.on_reach_end.emit()
            self.set_velocity(0, 0)

    def choose_next_point(self) -> int | None:
        """Выбирает следующую целевую точку пути."""
        self._target_point_ref -= 1
        logging.debug(f"Target Point: {self.path.points[self._target_point_ref]}")
        return self._target_point_ref
