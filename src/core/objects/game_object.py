import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent

from dataclasses import dataclass, field
from abc import abstractmethod

@dataclass
class Model:
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    rotation: float = 0.0

    @abstractmethod
    def update(self, delta_time: float):
        """Регулярно обновляет модель."""
        ...

@dataclass
class View:
    @abstractmethod
    def draw(self, screen: pygame.Surface, model):
        """Отрисовывает по модели."""
        ...

@dataclass
class Controller:
    model: Model

    @abstractmethod
    def handle_input(self, event: PygameEvent):
        """Читает pygame.event и уведомляет модель по Event"""
        ...

@dataclass
class GameObject:
    model: Model
    view: View
    controller: Controller