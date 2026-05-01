import pygame

from src.core.systems.input import InputManager
from src.core.systems.physics import PhysicsSystem
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene


class Game:
    def __init__(self, scene_class):
        # Input
        # Render
        # Show
        self.input: InputManager = InputManager()
        self.scene: Scene = scene_class()
        # self.physics = PhysicsSystem()
        self.renderer: Renderer = Renderer()
        self.paused: bool = False
        self.running: bool = True

        self.input.on_exit.subscribe(self.exit)

    def update(self, delta_time: float):
        # Input
        self.input.handle_input(self.scene)
        # Update
        self.scene.update(delta_time)

    def draw(self, screen: pygame.Surface):
        self.renderer.draw(screen, self.scene)

    def exit(self):
        self.running = False