from dataclasses import dataclass, field

import pygame
from pygame.math import Vector2

from src.core.objects.game_object import Model, View


@dataclass
class RectView(View):
    color: tuple[int, int, int] = (255, 255, 255)
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))

    def draw(self, screen: pygame.Surface, model: Model, local_position):
        rect = pygame.Rect(local_position.x, local_position.y, self.size.x, self.size.y)
        pygame.draw.rect(screen, self.color, rect)


@dataclass
class SpriteView(View):
    image_path: str = ""
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    _resized_image: pygame.Surface | None = None

    def __post_init__(self):
        if self.image_path:
            self._resized_image = pygame.transform.scale(
                self.il.load_image(self.image_path).surface, size=self.size
            )

    def draw(self, screen: pygame.Surface, model: Model, local_position):
        screen.blit(self._resized_image, dest=local_position)
