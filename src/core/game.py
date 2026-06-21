import pygame
from pygame.math import Vector2

from src.core.objects.camera import Camera
from src.core.singletones.audio_loader import AudioLoader, audio_loader
from src.core.singletones.event_bus import event_bus
from src.core.singletones.global_data import global_data
from src.core.systems.collision import CollisionSystem
from src.core.systems.debug_renderer import DebugRenderer
from src.core.systems.input import InputManager, cursor
from src.core.systems.movement import MovementSystem
from src.core.systems.renderer import Renderer
from src.core.systems.targeting import TargetingSystem
from src.core.systems.uniform_grid import UniformGrid


class Game:
    """Базовый класс для состояния игры."""

    def __init__(self, scene_class, window_size: tuple, debug: bool = False):
        """
        Args:
            scene_class: класс сцены инициализации.
            window_size: размер окна.
            debug: режим отладки (рендер коллизий, областей интерфейса).
        """
        # Системы
        self.input: InputManager = InputManager()
        self.movement = MovementSystem()
        self.camera: Camera = Camera(
            cursor,
            event_bus,
            size=Vector2(window_size),
        )
        self.uniform_grid = UniformGrid()
        self.collision = CollisionSystem(self.uniform_grid)
        self.targeting = TargetingSystem(self.uniform_grid)
        self.renderer: Renderer = Renderer()
        self.audio: AudioLoader = audio_loader
        self.debug: bool = debug
        self.debug_renderer: DebugRenderer = DebugRenderer()
        # Состояние
        self.paused: bool = False
        self.running: bool = True
        # Глобальные события
        self.input.on_exit.subscribe(self.exit)
        # Глобальные данные.
        self.global_data = global_data
        # Сцена.
        self.set_scene(scene_class)

    def update(self, delta_time: float):
        """Кадр игры, обновление всех систем."""
        # Input
        self.input.handle_input(self.scene, self.camera)
        # AI
        # Movement
        self.movement.update(self.scene, delta_time)
        # UniformGrid (очистка)
        self.uniform_grid.update(self.scene)
        # Collision
        self.collision.update(self.scene, delta_time)
        # Resolution (разрешение столкновений).
        self.collision.resolve(delta_time)
        # Targeting
        self.targeting.update(self.scene, delta_time)
        # Game Logic
        self.scene.update(delta_time)
        # Camera
        self.camera.handle_drag()
        # Cleanup
        self.scene.cleanup()
        # Add objects (после всей логики).
        self.scene.add_objects()

    def draw(self, screen: pygame.Surface):
        """Отрисовка элементов (отдельно от обновлений и логики)."""
        self.renderer.draw(screen, self.scene, self.camera)
        if self.debug:
            self.debug_renderer.draw(screen, self.scene, self.camera)

    def set_scene(self, scene_class):
        """Смена текущей сцены."""
        self.scene = scene_class(event_bus, self.audio, global_data, self.exit)
        self.scene.on_scene_changed.subscribe(self.set_scene)

    def exit(self):
        """Выход из игры."""
        self.running = False
