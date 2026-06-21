import pytest
from pygame.math import Vector2

from src.core.objects import (
    GameObject,
    PositionComponent,
)
from src.core.objects.scene import Scene
from src.core.systems.collision import CollisionSystem
from src.core.systems.uniform_grid import UniformGrid


def test_uniform_grid():
    uniform_grid = UniformGrid(50, 100)
    scene = Scene(None, None, None, None)
    obj1 = (
        GameObject()
        .add(PositionComponent(Vector2(10, 10), None))
    )
    obj2 = (
        GameObject()
        .add(PositionComponent(Vector2(99, 99), None))
    )
    scene.add_object(obj1)
    scene.add_object(obj2)
    scene.add_objects()
    uniform_grid.update(scene)
    # Сама сущность тоже считается.
    assert len(uniform_grid.query_rect(obj1, 1, 1)) == 2
    obj2.get(PositionComponent).position = Vector2(100, 99)
    uniform_grid.update(scene)
    assert len(uniform_grid.query_rect(obj1, 1, 1)) == 1
    obj2.get(PositionComponent).position = Vector2(1, 1)
    uniform_grid.update(scene)
    assert len(uniform_grid.query_rect(obj1, 1, 1)) == 2