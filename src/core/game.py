import pygame
from pygame.math import Vector2

from src.core.systems.camera import Camera
from src.core.systems.collision import CollisionSystem
from src.core.systems.input import InputManager
from src.core.systems.movement import MovementSystem
from src.core.systems.renderer import Renderer
from src.core.systems.scene import Scene
from src.core.systems.targeting import TargetingSystem
from src.core.systems.uniform_grid import UniformGrid


class Game:
    """Базовый класс для состояния игры."""

    WINDOW_SIZE = (720, 720)

    def __init__(self, scene_class):
        # Systems
        self.input: InputManager = InputManager()
        self.movement = MovementSystem()
        self.camera: Camera = Camera(
            size=Vector2(self.WINDOW_SIZE),
            cursor=self.input.cursor
        )
        self.uniform_grid = UniformGrid()
        self.collision = CollisionSystem(self.uniform_grid)
        self.targeting = TargetingSystem(self.uniform_grid)
        self.renderer: Renderer = Renderer()
        # State
        self.paused: bool = False
        self.running: bool = True
        # Global events
        self.input.on_exit.subscribe(self.exit)
        # Scene
        self.scene: Scene = scene_class(self.input.cursor, self.exit)

    def update(self, delta_time: float):
        # Input
        self.input.handle_input(self.scene, self.camera)
        # AI
        # Movement
        self.movement.update(self.scene, delta_time)
        # UniformGrid (очистка)
        self.uniform_grid.update(self.scene)
        # Collision
        self.collision.update(self.scene, delta_time)
        # Resolution
        self.collision.resolve(delta_time)
        # Targeting
        self.targeting.update(self.scene, delta_time)
        # Game Logic
        self.scene.update(delta_time)
        # Camera
        self.camera.handle_drag()
        # Cleanup
        self.scene.cleanup()
        # Add objects after all logics.
        self.scene.add_objects()

    def draw(self, screen: pygame.Surface):
        self.renderer.draw(screen, self.scene, self.camera)

    def exit(self):
        self.running = False
