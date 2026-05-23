from dataclasses import dataclass, field
from pygame.math import Vector2

from src.core.objects import *

@dataclass
class PathModel(Model):
    points: list[Vector2]

@dataclass
class PathBodyModel(KinematicBodyModel):
    """Модель объекта следования по пути."""
    path: PathModel = field(default_factory=lambda: PathModel(
        position=Vector2(0, 0), 
        points=list()
    ))
    point_radius: int = 3
    _target_point: Vector2 | None = None

    def update(self, delta_time: float):
        self.follow_path()

    def follow_path(self):
        """Следует по пути."""
        if self._target_point is not None:
            dx = self._target_point.x - self.position.x
            dy = self._target_point.y - self.position.y
            dist = dx**2 + dy**2
            min_dist = (self.point_radius)**2
            if dist <= min_dist:
                self._target_point = self.choose_next_point()
                print(self.position, "->", self._target_point)
            else:
                d = Vector2(dx, dy).normalize()
                self.set_velocity(d[0], d[1])
        elif self.path.points:
            print("DONT")
            self._target_point = self.choose_next_point()
        else:
            self.set_velocity(0, 0)

    def choose_next_point(self) -> Vector2 | None:
        """Выбирает следующую целевую точку пути."""
        return self.path.points.pop() if self.path.points else None