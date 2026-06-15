import logging
from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import *
from src.core.objects.event import Event


class PathComponent:
    def __init__(self, points: list):
        self.points = [Vector2(p) for p in points][::-1]


class PatrolComponent:
    """Модель компонента следования по пути."""
    def __init__(self, position, movement, path: PathComponent, point_radius: int = 3):
        self.position = position
        self.movement = movement
        self.path = path
        self.point_radius = point_radius
        self._target_point_ref = len(self.path.points) - 1
        self.on_start_patrol: Event = Event()
        self.on_reached_end: Event = Event()
        self.start_patrol()

    def start_patrol(self):
        self.on_start_patrol.emit(self.path.points[self._target_point_ref])
        self.position.position = self.path.points[self._target_point_ref]

    def update(self, delta_time):
        self.follow_path()

    def follow_path(self):
        """Следует по пути."""
        if self._target_point_ref >= 0:
            target_point = self.path.points[self._target_point_ref]
            dx = target_point.x - self.position.position.x
            dy = target_point.y - self.position.position.y
            dist = dx**2 + dy**2
            min_dist = (self.point_radius) ** 2
            if dist <= min_dist:
                self.choose_next_point()
                # print(self.position, "->", target_point)
            else:
                d = Vector2(dx, dy).normalize()
                self.movement.set_velocity(d[0], d[1])
        elif self._target_point_ref == -1:
            self.choose_next_point()
        else:
            self.on_reached_end.emit()
            self.movement.set_velocity(0, 0)

    def choose_next_point(self) -> int | None:
        """Выбирает следующую целевую точку пути."""
        self._target_point_ref -= 1
        # logging.debug(f"Target Point: {self.path.points[self._target_point_ref]}")
        return self._target_point_ref
