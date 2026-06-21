import pytest
from pygame.math import Vector2

from src.core.objects.camera import ZOOMES, Camera
from src.core.singletones.event_bus import EventBus
from src.core.systems.input import Cursor


def test_base():
    event_bus = EventBus()
    var = 0
    def func(event):
        nonlocal var
        var = 10
    event_bus.subscribe("on_smth_happened", func)
    event_bus.fire("on_smth_happened")
    assert var == 10

def test_priority():
    event_bus = EventBus()
    var = 0
    def func1(event):
        nonlocal var
        var = 5
        event.stop()
    def func2(event):
        nonlocal var
        var = 10
        event.stop()
    event_bus.subscribe("on_smth_happened", func1, priority=2)
    event_bus.subscribe("on_smth_happened", func2, priority=1)
    event_bus.fire("on_smth_happened")
    assert var == 5

def test_refs_deletion():
    event_bus = EventBus()
    class Example:
        def func(self):
            print("Привет!")
    example = Example()
    event_bus.subscribe("on_smth_happened", example.func)
    example = 5
    event_bus.fire("on_smth_happened")
    event_bus.fire("on_smth_happened")
    assert len(event_bus.listeners["on_smth_happened"]) == 0