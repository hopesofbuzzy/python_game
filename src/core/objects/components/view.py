import logging
from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.objects.game_object import GameObject
from src.core.singletones.image_loader import Image
from src.core.singletones.image_loader import image_loader as il


class RectComponent:
    """Отрисовщик прямоугольников в мире."""
    def __init__(self, color: tuple[int, int, int], size: Vector2, centred: bool):
        self.color = color
        self.size = size
        self.centred = centred

    def get_centred_local_position(self, local_position, zoom):
        """Возвращает отцентрованную экранную позицию прямоугольника."""
        return local_position - (self.size * zoom // 2)

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        if self.centred:
            local_position = self.get_centred_local_position(
                local_position,
                camera.zoom
            )
        rect = pygame.Rect(
            local_position.x,
            local_position.y,
            self.size.x * camera.zoom,
            self.size.y * camera.zoom
        )
        pygame.draw.rect(screen, self.color, rect)

class SpriteComponent:
    """Отрисовщик спрайтов в мире."""
    def __init__(self, image_path: str, size: Vector2, centred: bool):
        self.image_path = image_path
        self.centred = centred
        self.size = size
        self._original_image = il.load_image(self.image_path)
        self._scaled_images: dict[float, pygame.Surface] = dict()

    def __post_init__(self):
        if self.image_path:
            try:
                self._original_image = il.load_image(self.image_path)
            except:
                ...
        else:
            logging.warning(f"SpriteView не содержит изображения для визуализации!")

    def get_scaled_image(self, size: float):
        if isinstance(self._original_image, Image):
            if size not in self._scaled_images:
                self._scaled_images[size] = pygame.transform.scale(
                    self._original_image.surface, size=self.size*size
                ).convert_alpha()
            return self._scaled_images[size]

    def get_centred_local_position(self, local_position, zoom):
        """Возвращает отцентрованную экранную позицию спрайта."""
        return local_position - (self.size * zoom // 2)

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        scaled_image = self.get_scaled_image(camera.zoom)
        if self.centred:
            local_position = self.get_centred_local_position(
                local_position,
                camera.zoom
            )
        if scaled_image:
            screen.blit(scaled_image, dest=local_position)
