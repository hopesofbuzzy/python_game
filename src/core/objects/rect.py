import pygame
from pygame.math import Vector2
from dataclasses import dataclass

from src.core.objects.game_object import View, Model

@dataclass
class RectView(View):
    color: tuple[int, int, int] = (255, 255, 255)

    def draw(
            self,
            screen: pygame.Surface,
            model: Model 
        ):
        pos = model.position
        size = model.size
        rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        pygame.draw.rect(screen, self.color, rect)