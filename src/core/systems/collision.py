from pygame.math import Vector2
from math import sqrt
from itertools import combinations
from dataclasses import dataclass

from src.core.systems.scene import Scene
from src.core.systems.uniform_grid import UniformGrid
from src.core.objects import *

@dataclass
class Overlap:
    """
        Контейнер данных о направлении и глубине пересечения
        коллизий.
    """
    # Направление разрешения
    nx: float
    ny: float
    # Глубина
    depth: float

class CollisionSystem:
    """
        Система коллизий и столкновений.
        Регулирует состояние коллизий и столкновений.
        Эффективно разрешает столкновения.

        Владеет UniformGrid x Collisions (Single responsibility).
    """
    def __init__(self):
        self.collisions: list[tuple] = []
        self.uniform_grid = UniformGrid()

    def update_uniform_grid(self, scene: Scene):
        """Очистка и пересоздание UniformGrid."""
        self.uniform_grid.clear()
        for object in scene.object_registry.values():
            self.uniform_grid.insert(object)

    def update(self, scene: Scene, delta_time: float):
        """Проверка коллизий и определение столкновений."""
        checks = 0
        for object in scene.object_registry.values():
            others = self.uniform_grid.query(object)
            for other in others:
                if object._uid >= other._uid:
                    continue
                checks += 1
                if (
                    isinstance(object.model, Collidable)
                    and isinstance(other.model, Collidable)
                ):
                    overlap = self.check_overlap(object.model, other.model)
                    if overlap:
                        self.collisions.append(
                            (
                                object.model,
                                other.model,
                                overlap
                            )
                        )
        # print(checks)

    @staticmethod
    def circles_collide(pos1, r1, pos2, r2) -> Overlap | None:
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        dist = dx**2 + dy**2
        min_dist = (r1 + r2)**2
        if dist <= min_dist:
            n = Vector2(dx, dy).normalize()
            return Overlap(nx=n.x, ny=n.y, depth=(r1+r2)-sqrt(dist))

    @staticmethod
    def aabb_collide(pos1, size1, pos2, size2) -> Overlap | None:
        if (
            pos1.x <= pos2.x + size2.x
            and pos2.x <= pos1.x + size1.x
            and pos1.y <= pos2.y + size2.y
            and pos2.y <= pos1.y + size1.y
        ):
            dx = pos1.x - pos2.x + (size1.x - size2.x) / 2
            adx = abs(dx)
            depth_x = (size1.x + size2.x) / 2 - adx
            dy = pos1.y - pos2.y + (size1.y - size2.y) / 2
            ady = abs(dy)
            n = Vector2(dx, dy).normalize()

            if adx > ady:
                return Overlap(nx=n.x, ny=0, depth=depth_x)
            depth_y = (size1.y + size2.y) / 2 - ady
            return Overlap(nx=0, ny=n.y, depth=depth_y)

    def check_overlap(self, object: Collidable, other: Collidable):
        obj = object.shape
        oth = other.shape
        obj_position = object.position + obj.position
        oth_position = other.position + oth.position
        # Circle x Circle
        if isinstance(obj, CircleShape) and isinstance(oth, CircleShape):
            return self.circles_collide(
                obj_position,
                obj.radius,
                oth_position,
                oth.radius
            )
        # Rect x Rect
        elif isinstance(obj, RectShape) and isinstance(oth, RectShape):
            return self.aabb_collide(
                obj_position,
                obj.size,
                oth_position,
                oth.size
            )

    def resolve(self, delta_time: float):
        """Разрешение столкновений."""
        for object, other, overlap in self.collisions:
            if isinstance(object, KinematicBodyModel) and object.velocity:
                object.position += Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
            if isinstance(other, KinematicBodyModel) and other.velocity:
                other.position -= Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
        self.collisions = []