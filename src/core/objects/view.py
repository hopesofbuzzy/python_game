import logging
from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.objects.game_object import Model, View
from src.core.systems.images import Image


@dataclass
class RectView(View):
    color: tuple[int, int, int] = (255, 255, 255)
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    centred: bool = False

    def get_centred_local_position(self, local_position, zoom):
        return local_position - (self.size * zoom // 2)

    def draw(self, screen: pygame.Surface, model: Model, local_position, zoom):
        if self.centred:
            local_position = self.get_centred_local_position(local_position, zoom)
        rect = pygame.Rect(
            local_position.x,
            local_position.y,
            self.size.x * zoom,
            self.size.y * zoom
        )
        pygame.draw.rect(screen, self.color, rect)


@dataclass
class SpriteView(View):
    image_path: str = ""
    centred: bool = False
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    _original_image: Image | None = None
    _scaled_images: dict[float, pygame.Surface] = field(default_factory=dict)

    def __post_init__(self):
        if self.image_path:
            try:
                self._original_image = self.il.load_image(self.image_path)
            except:
                ...
        else:
            logging.warning(f"SpriteView не содержит изображения для визуализации!")

    def get_scaled_image(self, size: float):
        if isinstance(self._original_image, Image):
            if size not in self._scaled_images:
                self._scaled_images[size] = pygame.transform.scale(
                    self._original_image.surface, size=self.size*size
                )
            return self._scaled_images[size]

    def get_centred_local_position(self, local_position, zoom):
        return local_position - (self.size * zoom // 2)

    def draw(self, screen: pygame.Surface, model: Model, local_position, zoom):
        scaled_image = self.get_scaled_image(zoom)
        if self.centred:
            local_position = self.get_centred_local_position(local_position, zoom)
        if scaled_image:
            screen.blit(scaled_image, dest=local_position)
