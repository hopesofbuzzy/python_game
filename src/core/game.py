import pygame

from src.core.systems.input import InputManager
from src.core.systems.physics import PhysicsSystem
from src.core.systems.movement import MovementSystem
from src.core.systems.collision import CollisionSystem
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene


class Game:
    """Базовый класс для состояния игры."""
    def __init__(self, scene_class):
        self.input: InputManager = InputManager()
        self.scene: Scene = scene_class()
        # self.physics = PhysicsSystem()
        self.movement = MovementSystem()
        self.collision = CollisionSystem()
        self.renderer: Renderer = Renderer()
        self.paused: bool = False
        self.running: bool = True

        self.input.on_exit.subscribe(self.exit)

    def update(self, delta_time: float):
        # Input
        self.input.handle_input(self.scene)
        # AI
        # Movement
        self.movement.update(self.scene, delta_time)
        # Collision
        self.collision.update(self.scene, delta_time)
        # Resolution
        self.collision.resolve(self.scene, delta_time)
        # Game Logic
        self.scene.update(delta_time)
        # Cleanup

    def draw(self, screen: pygame.Surface):
        self.renderer.draw(screen, self.scene)

    def exit(self):
        self.running = False