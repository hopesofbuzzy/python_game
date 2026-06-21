from pygame.math import Vector2
import pytest

from src.core.objects.camera import Camera, ZOOMES
from src.core.systems.input import Cursor
from src.core.singletones.event_bus import EventBus

WINDOW_SIZE = Vector2(600, 600)

def test_zoom():
    cursor = Cursor()
    event_bus = EventBus()
    camera = Camera(cursor, event_bus, WINDOW_SIZE)
    for _ in range(5):
        event_bus.fire("on_mouse_wheel", True)
    assert camera.zoom == ZOOMES[len(ZOOMES)-1]
    for _ in range(8):
        event_bus.fire("on_mouse_wheel", False)
    assert camera.zoom == ZOOMES[0]

def test_local_global_position():
    cursor = Cursor()
    event_bus = EventBus()
    camera = Camera(cursor, event_bus, WINDOW_SIZE)
    camera.zoom = 1.5
    camera.position = Vector2(100, 200)
    assert camera.to_local(Vector2(100, 200)) == Vector2(0, 0)
    assert camera.to_local(Vector2(120, 220)) == Vector2(30, 30)
    assert camera.to_local(Vector2(50, 200)) == Vector2(-75, 0)
    camera.zoom = 2.0
    assert camera.to_local(Vector2(50, 200)) == Vector2(-100, 0)
    assert camera.to_global(Vector2(10, 10)) == Vector2(105, 205)

def test_visible_range():
    cursor = Cursor()
    event_bus = EventBus()
    camera = Camera(cursor, event_bus, WINDOW_SIZE)
    camera.position = Vector2(100, 0)
    assert camera.get_visible_range(33, 10, 10) == (3, 9, 0, 9)
    assert camera.get_visible_range(100, 5, 5) == (1, 4, 0, 4)