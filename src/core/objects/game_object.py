import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent

from dataclasses import dataclass, field
from abc import abstractmethod

@dataclass
class Model:
    position: Vector2

    @abstractmethod
    def update(self, delta_time: float):
        """Регулярно обновляет модель."""
        ...

@dataclass
class View:
    @abstractmethod
    def draw(self, screen: pygame.Surface, model, local_position):
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
    view: View | None = None
    controller: Controller | None = None
    _active: bool = True
    _uid: int = -1

    def free(self):
        self._active = False