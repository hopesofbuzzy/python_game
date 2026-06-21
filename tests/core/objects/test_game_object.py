from pygame.event import Event as PygameEvent

from src.core.objects import GameObject
from src.core.systems.input import Cursor


class ExampleComponent():
    def __init__(self):
        self.got_input = False
        self.got_update = False
        self.got_draw = False

    def handle_input(self, event, cursor):
        self.got_input = True

    def update(self, delta_time):
        self.got_update = True

    def draw(self, screen, size, local_position, camera):
        self.got_draw = True

def test_components():
    obj = GameObject()
    obj.add(ExampleComponent())
    obj.handle_input(PygameEvent(1), Cursor())
    obj.update(0.1)
    obj.draw(None, None, None, None)
    comp = obj.get(ExampleComponent)
    assert comp.got_input and comp.got_update and comp.got_draw