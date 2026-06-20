import logging

import pygame


DEFAULT_BAR_COLOR = (255, 70, 70)
DEFAULT_EMPTY_BAR_COLOR = (127, 35, 35)

class BarComponent:
    """Отрисовщик шкалы отображения значения."""
    def __init__(
            self,
            start: int,
            max: int,
            color: tuple = DEFAULT_BAR_COLOR
    ):
        self.value = start
        if start > max:
            self.value = max
        self.max = max
        self.color = color

    def set_value(self, value: int):
        self.value = value
        logging.debug(f"Установленое значение шкалы: {self.value} / {self.max}")

    def draw(self, screen: pygame.Surface, size, local_position, zoom):
        border = size.x * zoom * (self.value / self.max)
        full_rect = pygame.Rect(
            local_position.x,
            local_position.y,
            border,
            size.y * zoom
        )
        empty_rect = pygame.Rect(
            local_position.x + border,
            local_position.y,
            size.x * zoom * (1 - self.value / self.max),
            size.y * zoom
        )
        pygame.draw.rect(screen, self.color, full_rect)
        pygame.draw.rect(screen, DEFAULT_EMPTY_BAR_COLOR, empty_rect)