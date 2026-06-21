import pygame

from src.core.objects.event import Event


class KeyControllerComponent:
    def __init__(self):
        self.on_key_pressed: Event = Event()

    def handle_input(self, event, cursor):
        match event.type:
            case pygame.KEYDOWN:
                if event.dict["unicode"].isdigit():
                    self.on_key_pressed.emit(event.dict["unicode"])
