import pytest
from pygame.math import Vector2

from src.core.objects import (
    CollisionComponent,
    GameObject,
    MovementComponent,
    PositionComponent,
    RectShape,
)
from src.core.objects.scene import Scene
from src.core.systems.collision import CollisionSystem
from src.core.systems.uniform_grid import UniformGrid


def test_collision_search():
    uniform_grid = UniformGrid()
    collision = CollisionSystem(uniform_grid)
    scene = Scene(None, None, None, None)
    # obj1 и obj2 пересекаются.
    obj1 = (
        GameObject()
        .add(PositionComponent(Vector2(10, 10), None))
    )
    obj1.add(CollisionComponent(
        obj1,
        RectShape(
            Vector2(0, 0),
            Vector2(50, 50),
            True
    )))
    obj2 = (
        GameObject()
        .add(PositionComponent(Vector2(55, 55), None))
        .add(MovementComponent(Vector2(0, 0), 100))
    )
    obj2.add(CollisionComponent(
        obj1,
        RectShape(
            Vector2(0, 0),
            Vector2(40, 40),
            True
    )))
    scene.add_object(obj1)
    scene.add_object(obj2)
    scene.add_objects()
    uniform_grid.update(scene)
    collision.update(scene, 0)
    assert len(collision.collisions) == 1
    # Теперь не пересекаются
    obj2.get(PositionComponent).position = Vector2(60, 60)
    uniform_grid.update(scene)
    collision.update(scene, 0)
    assert len(collision.collisions) == 0