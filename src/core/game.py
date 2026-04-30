import pygame

from src.core.systems.input import InputManager
from src.core.systems.physics import PhysicsSystem
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene


class Game:
    def __init__(self, scene: Scene):
        # Input
        # Render
        # Show
        self.input: InputManager = InputManager()
        self.physics = PhysicsSystem()
        self.renderer = Renderer()
        self.scene: Scene = scene
        self.paused: bool = False
        self.running: bool = True

        self.input.on_exit.subscribe(self.exit)

    def update(self, delta_time: float):
        # Input
        self.input.handle_input()

    def draw(self, screen: pygame.Surface):
        screen.fill("purple")
        rect = pygame.Rect(100, 100, 100, 100)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        # self.renderer.draw()

    def exit(self):
        self.running = False