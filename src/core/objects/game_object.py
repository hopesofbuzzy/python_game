import pygame
from pygame.math import Vector2
from pygame.event import Event as PygameEvent

from dataclasses import dataclass, field
from abc import abstractmethod

from src.core.systems.images import ImageLoader

@dataclass
class Model:
    local_position: Vector2
    parent = None
    # Инъекция метода удаления объекта в Scene.
    free = None

    @property
    def position(self):
        if self.parent:
            return self.local_position + self.parent.position
        else:
            return self.local_position

    @position.setter
    def position(self, value):
        if self.parent:
            self.local_position =  value - self.parent.position
        else:
            self.local_position = value

    @abstractmethod
    def update(self, delta_time: float):
        """Регулярно обновляет модель."""
        ...

@dataclass
class View:
    # Инъекция загрузчика изображений в EntityFactory.
    il: ImageLoader

    @abstractmethod
    def draw(self, screen: pygame.Surface, model, local_position):
        """Отрисовывает по модели."""
        ...

@dataclass
class Controller:
    model: Model
    # Инъекция объекта курсора в EntityFactory.
    cursor = None

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
