from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.systems.images import ImageLoader
from src.core.systems.input import Cursor


@dataclass
class Model:
    local_position: Vector2
    parent: Optional["Model"] = None
    # Инъекция метода удаления объекта в Scene.
    free: Optional[Callable] = None

    def __post_init__(self):
        self.local_position = self.local_position.copy()

    @property
    def position(self):
        if self.parent:
            return self.local_position + self.parent.position
        else:
            return self.local_position

    @position.setter
    def position(self, value):
        if self.parent:
            self.local_position = value - self.parent.position
        else:
            self.local_position = value.copy()

    @abstractmethod
    def update(self, delta_time: float):
        """Регулярно обновляет модель."""
        ...


@dataclass
class View:
    # Инъекция загрузчика изображений (ImageLoader) в EntityFactory.
    il: Optional[ImageLoader] = None
    parent: Optional["Model"] = None

    @abstractmethod
    def draw(self, screen: pygame.Surface, model, local_position, zoom):
        """Отрисовывает по модели."""
        ...


@dataclass
class Controller:
    model: Model
    # Инъекция объекта курсора в EntityFactory.
    cursor: Cursor

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
