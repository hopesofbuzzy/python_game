import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent

from dataclasses import dataclass
from abc import abstractmethod

class Model:
    def __init__(
            self,
            position: Vector2 = Vector2(0, 0),
            rotation: float = 0.0,
            size: Vector2 = Vector2(0, 0)
        ):
        self.position = position
        # Радианы.
        self.rotation: float = rotation
        self.size = size

    @abstractmethod
    def update(self, delta_time: float):
        """Регулярно обновляет модель."""
        ...

class View:
    @abstractmethod
    def draw(self, screen: pygame.Surface, model: Model):
        """Отрисовывает по модели."""
        ...

class Controller:
    def __init__(self, model: Model):
        self.model = model

    @abstractmethod
    def handle_input(self, event: PygameEvent):
        """Читает pygame.event и уведомляет модель по Event"""
        ...

@dataclass
class GameObject:
    model: Model
    view: View
    controller: Controller