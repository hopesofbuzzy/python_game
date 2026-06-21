import logging

import pygame
from pygame.event import Event as PygameEvent
from pygame.math import Vector2

from src.core.objects.components import PositionComponent
from src.core.systems.input import Cursor


class CursorCircleComponent:
    """Компонент отрисовки полупрозрачной области вокруг курсора."""
    def __init__(self, entity, radius: int, color: tuple):
        self.radius = radius
        self.color = color
        self.entity = entity
        self.circle_surfaces = dict()

    def handle_input(self, event: PygameEvent, cursor: Cursor):
        if cursor.global_pos != self.entity.get(PositionComponent).position:
            logging.info("Смена")
            self.entity.get(PositionComponent).position = cursor.global_pos

    def get_centred_local_position(self, local_position, zoom):
        local_position.x -= (self.radius * zoom)
        local_position.y -= (self.radius * zoom)
        return local_position

    def get_scaled_circle(self, size):
        if not size in self.circle_surfaces:
            radius = self.radius * size
            self.circle_surfaces[size] = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA
            ).convert_alpha()
            pygame.draw.circle(
                self.circle_surfaces[size],
                self.color,
                (radius, radius),
                radius)
        return self.circle_surfaces[size]

    def draw(self, screen, size, local_position, camera):
        screen.blit(
            self.get_scaled_circle(camera.zoom),
            self.get_centred_local_position(local_position, camera.zoom)
        )