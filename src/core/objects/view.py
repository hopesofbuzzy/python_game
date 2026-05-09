import pygame
from pygame.math import Vector2
from dataclasses import dataclass, field

from src.core.objects.game_object import View, Model
from src.core.systems.images import Image

@dataclass
class RectView(View):
    color: tuple[int, int, int] = (255, 255, 255)
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))

    def draw(
            self,
            screen: pygame.Surface,
            model: Model 
        ):
        pos = model.position
        rect = pygame.Rect(pos.x, pos.y, self.size.x, self.size.y)
        pygame.draw.rect(screen, self.color, rect)

@dataclass
class SpriteView(View):
    image: Image
    size: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    _resized_image: pygame.Surface | None = None

    def __post_init__(self):
        self._resized_image = pygame.transform.scale(
            self.image.surface,
            size=self.size
        )

    def draw(
        self,
        screen: pygame.Surface,
        model: Model
    ):
        pos = model.position
        screen.blit(self._resized_image, dest=pos)