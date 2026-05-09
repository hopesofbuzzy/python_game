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
    filename: str
    image: Image | None = None

    def draw(
        self,
        screen: pygame.Surface,
        model: Model
    ):
        ...

    def __del__(self):
        image.refcount -= 1