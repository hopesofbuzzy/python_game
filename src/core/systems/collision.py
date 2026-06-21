import logging
from dataclasses import dataclass
from math import sqrt

from pygame.math import Vector2

from src.core.objects import (
    CircleShape,
    CollisionComponent,
    GameObject,
    MovementComponent,
    PositionComponent,
    RectShape,
    Scene,
)


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
        """Проверка коллизий объектов сцены и определение столкновений."""
        checks = 0
        self.collisions = []
        for object in scene.object_registry.values():
            if object.has(PositionComponent, CollisionComponent):
                others = self.uniform_grid.query_rect(object, 2, 2)
                mask_tag = object.get(CollisionComponent).mask_tag
                for other in others:
                    if not (
                        other.has(MovementComponent)
                        or object.has(MovementComponent)
                    ):
                        continue
                    # Проверка целевых тегов коллизий
                    # (простая маска по командам).
                    if mask_tag and mask_tag not in other.tags:
                        continue
                    if other.has(PositionComponent, CollisionComponent):
                        # Некоторым объектам не нужно вычислять выталкивание.
                        resolve = False
                        if (
                            object.get(CollisionComponent).resolvable
                            and other.get(CollisionComponent).resolvable
                        ):
                            resolve = True
                        # Их мы вычисляем по упрощённой схеме.
                        if object.uid <= other.uid:
                            continue
                        checks += 1
                        overlap = self.check_overlap(
                            object, other, resolve=resolve
                        )
                        if overlap:
                            self.collisions.append(
                                (object, other, overlap, resolve)
                            )

    @staticmethod
    def circles_collide(pos1, r1, pos2, r2, resolve) -> Overlap | None | bool:
        """
        Проверка коллизий у окружностей.

        Args:
            pos: позиции форм.
            r: радиусы форм.
            resolve: вычисление направления выталкивания,
        """
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
    def aabb_collide(
        pos1, size1, pos2, size2, resolve
    ) -> Overlap | None | bool:
        """
        Проверка коллизий у прямоугольников.

        Args:
            pos: позиции форм.
            size: размеры форм.
            resolve: вычисление направления выталкивания,
        """
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
            n = Vector2(1, 0) if dx == dy == 0 else Vector2(dx, dy).normalize()

            if adx > ady:
                return Overlap(nx=n.x, ny=0, depth=depth_x)
            depth_y = (size1.y + size2.y) / 2 - ady
            return Overlap(nx=0, ny=n.y, depth=depth_y)

    def check_overlap(
        self, object: GameObject, other: GameObject, resolve: bool
    ) -> Overlap | None | bool:
        """Проверка пересечения коллизий двух объектов."""
        obj_shape = object.get(CollisionComponent).shape
        oth_shape = other.get(CollisionComponent).shape
        obj_position = (
            object.get(PositionComponent).position + obj_shape.position
        )
        oth_position = (
            other.get(PositionComponent).position + oth_shape.position
        )
        # Circle x Circle
        if isinstance(obj_shape, CircleShape) and isinstance(
            oth_shape, CircleShape
        ):
            return self.circles_collide(
                obj_position,
                obj_shape.radius,
                oth_position,
                oth_shape.radius,
                resolve,
            )
        # Rect x Rect
        elif isinstance(obj_shape, RectShape) and isinstance(
            oth_shape, RectShape
        ):
            return self.aabb_collide(
                obj_position,
                obj_shape.size,
                oth_position,
                oth_shape.size,
                resolve,
            )

    def resolve(self, delta_time: float):
        """Разрешение всех найденных столкновений (выталкивание)."""
        for object, other, overlap, resolve in self.collisions:
            if resolve:
                if object.has(MovementComponent):
                    object.get(PositionComponent).position += (
                        Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
                    )
                if other.has(MovementComponent):
                    other.get(PositionComponent).position -= (
                        Vector2(overlap.nx, overlap.ny) * overlap.depth * 0.5
                    )
            object.get(CollisionComponent).handle_collision(other)
            other.get(CollisionComponent).handle_collision(object)
        self.collisions = []
