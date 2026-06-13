from dataclasses import dataclass
from math import sqrt

from pygame.math import Vector2

from src.core.objects import *
from src.core.systems.scene import Scene


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

    def __init__(self, uniform_grid):
        self.collisions: list[tuple] = []
        self.uniform_grid = uniform_grid

    def update(self, scene: Scene, delta_time: float):
        """Проверка коллизий и определение столкновений."""
        checks = 0
        for object in scene.object_registry.values():
            if isinstance(object.model, Collidable):
                others = self.uniform_grid.query_rect(object, 1, 1)
                for other in others:
                    if isinstance(other.model, Collidable):
                        # Некоторым объектам не нужно вычислять выталкивание.
                        resolve = False
                        if other.model.resolvable and object.model.resolvable:
                            resolve = True
                        # Их мы вычисляем по упрощённой схеме.
                        if object.uid >= other.uid:
                            continue
                        checks += 1
                        overlap = self.check_overlap(
                            object.model, other.model, resolve=resolve
                        )
                        if overlap:
                            self.collisions.append(
                                (object.model, other.model, overlap, resolve)
                            )
        # print(checks)

    @staticmethod
    def circles_collide(pos1, r1, pos2, r2, resolve) -> Overlap | None | bool:
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        dist = dx**2 + dy**2
        min_dist = (r1 + r2) ** 2
        if dist <= min_dist:
            if not resolve:
                return True
            n = Vector2(dx, dy).normalize()
            return Overlap(nx=n.x, ny=n.y, depth=(r1 + r2) - sqrt(dist))

    @staticmethod
    def aabb_collide(pos1, size1, pos2, size2, resolve) -> Overlap | None | bool:
        if (
            pos1.x <= pos2.x + size2.x
            and pos2.x <= pos1.x + size1.x
            and pos1.y <= pos2.y + size2.y
            and pos2.y <= pos1.y + size1.y
        ):
            if not resolve:
                return True
            dx = pos1.x - pos2.x + (size1.x - size2.x) / 2
            adx = abs(dx)
            depth_x = (size1.x + size2.x) / 2 - adx
            dy = pos1.y - pos2.y + (size1.y - size2.y) / 2
            ady = abs(dy)
            # Выталкивание в случае идеального перекрытия.
            if dx == dy == 0:
                n = Vector2(1, 0)
            else:
                n = Vector2(dx, dy).normalize()

            if adx > ady:
                return Overlap(nx=n.x, ny=0, depth=depth_x)
            depth_y = (size1.y + size2.y) / 2 - ady
            return Overlap(nx=0, ny=n.y, depth=depth_y)

    def check_overlap(
        self, object: Collidable, other: Collidable, resolve: bool
    ) -> Overlap | None | bool:
        obj = object.shape
        oth = other.shape
        obj_position = object.position + obj.position
        oth_position = other.position + oth.position
        # Circle x Circle
        if isinstance(obj, CircleShape) and isinstance(oth, CircleShape):
            return self.circles_collide(
                obj_position, obj.radius, oth_position, oth.radius, resolve
            )
        # Rect x Rect
        elif isinstance(obj, RectShape) and isinstance(oth, RectShape):
            return self.aabb_collide(
                obj_position, obj.size, oth_position, oth.size, resolve
            )

    def resolve(self, delta_time: float):
        """Разрешение столкновений."""
        for object, other, overlap, resolve in self.collisions:
            if resolve:
                if isinstance(object, KinematicBodyModel) and object.velocity:
                    object.position += (
                        Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
                    )
                if isinstance(other, KinematicBodyModel) and other.velocity:
                    other.position -= (
                        Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
                    )
            object.handle_collision(other)
            other.handle_collision(object)
        self.collisions = []
