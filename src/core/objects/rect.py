import pygame
from pygame.math import Vector2

from src.core.objects.game_object import View, Model

class RectView(View):
    def __init__(self, color: tuple[int, int, int]):
        super().__init__()
        self.color = color

    def draw(
            self,
            screen: pygame.Surface,
            model: Model 
        ):
        pos = model.position
        size = model.size
        rect = pygame.Rect(pos.x, pos.y, size.x, size.y)
        pygame.draw.rect(screen, self.color, rect)