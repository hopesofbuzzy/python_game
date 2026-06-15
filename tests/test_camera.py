import pytest
from pygame.math import Vector2

from src.core.objects.camera import Camera
from src.core.systems.input import Cursor


def test_camera():
    """Проверка инициализации камеры, зума"""
    cursor = Cursor()
    camera = Camera(cursor)
    for _ in range(10):
        cursor.on_mouse_wheel.emit(True)
    assert camera.zoom == camera.ZOOMES[len(camera.ZOOMES)-1]
    for _ in range(10):
        cursor.on_mouse_wheel.emit(False)
    assert camera.zoom == camera.ZOOMES[0]