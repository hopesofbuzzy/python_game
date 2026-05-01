import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent

from dataclasses import dataclass
from abc import abstractmethod

class Model:
    def __init__(self):
        self.position: Vector2 = Vector2(0, 0)
        # Радианы.
        self.rotation: float = 0
        self.size: Vector2 = Vector2(0, 0)

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
    def __init__(self, model: Model, view: View):
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