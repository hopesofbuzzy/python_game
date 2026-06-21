from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.objects import GameObject
from src.core.objects.components import PositionComponent


def test_position():
    parent_obj = (
        GameObject()
        .add(PositionComponent(Vector2(100, 100), None))
    )
    obj = (
        GameObject()
        .add(PositionComponent(Vector2(1, -2), parent_obj))
    )
    assert obj.get(PositionComponent).position == Vector2(101, 98)