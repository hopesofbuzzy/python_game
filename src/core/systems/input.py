import pygame

from src.core.systems.event import Event
from src.core.systems.scene import Scene

class InputManager:
    def __init__(self):
        self.on_exit = Event()

    def handle_input(self, scene: Scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_exit.emit()
            for object in scene.object_registry.values():
                object.controller.handle_input(event)
            scene.handle_input(event)