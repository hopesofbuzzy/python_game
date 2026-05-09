import pygame

from src.core.systems.input import InputManager
from src.core.systems.physics import PhysicsSystem
from src.core.systems.movement import MovementSystem
from src.core.systems.collision import CollisionSystem
from src.core.systems.images import ImageRegistry
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene


class Game:
    """Базовый класс для состояния игры."""
    def __init__(self, scene_class):
        # Systems
        self.input: InputManager = InputManager()
        self.scene: Scene = scene_class()
        self.movement = MovementSystem()
        self.collision = CollisionSystem()
        self.renderer: Renderer = Renderer()
        # Registries
        self.image_registry = ImageRegistry()
        # State
        self.paused: bool = False
        self.running: bool = True
        # Global events
        self.input.on_exit.subscribe(self.exit)

    def update(self, delta_time: float):
        # Input
        self.input.handle_input(self.scene)
        # AI
        # Movement
        self.movement.update(self.scene, delta_time)
        # UniformGrid (очистка)
        self.collision.update_uniform_grid(self.scene)
        # Collision
        self.collision.update(self.scene, delta_time)
        # Resolution
        self.collision.resolve(delta_time)
        # Game Logic
        self.scene.update(delta_time)
        # Cleanup
        self.scene.cleanup()

    def draw(self, screen: pygame.Surface):
        self.renderer.draw(screen, self.scene)

    def exit(self):
        self.running = False