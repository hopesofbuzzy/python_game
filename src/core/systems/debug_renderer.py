import logging

import pygame
from pygame.math import Vector2

from src.core.systems.scene import Scene
from src.core.systems.camera import Camera
from src.core.objects.collidable import (
    Collidable,
    CollisionShape,
    CircleShape,
    RectShape
)

COLLISION_COLOR = (255, 127, 80)
POSITION_POINT_RADIUS = 3
POSITION_POINT_COLOR = (255, 127, 255)

class DebugRenderer:
    """
        Визуальная отладка коллизий, позиций.

        Отрисовка происходит исключительно тут во избежание
        нарушения SRP.
    """
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Camera):
        for object in scene.object_registry.values():
            if isinstance(object.model, Collidable):
                shape = object.model.shape
                if isinstance(shape, RectShape):
                    self.draw_collision_rect(
                        screen,
                        camera.to_local(object.model.position + shape.position),
                        shape,
                        camera.zoom
                    )
                elif isinstance(shape, CircleShape):
                    self.draw_collision_circle(
                        screen,
                        camera.to_local(object.model.position + shape.position),
                        shape,
                        camera.zoom
                    )
            self.draw_position_point(
                screen,
                camera.to_local(object.model.position),
                camera.zoom
            )

    def draw_collision_rect(
            self,
            screen: pygame.Surface,
            local_position: Vector2,
            shape: RectShape,
            zoom: float
        ):
        rect = pygame.Rect(
            local_position.x,
            local_position.y,
            shape.size.x * zoom,
            shape.size.y * zoom
        )
        pygame.draw.rect(screen, COLLISION_COLOR, rect)


    def draw_collision_circle(
            self,
            screen: pygame.Surface,
            local_position: Vector2,
            shape: CircleShape,
            zoom: float
        ):
        pygame.draw.circle(
            screen,
            COLLISION_COLOR,
            local_position,
            shape.radius * zoom
        )

    def draw_position_point(
            self,
            screen: pygame.Surface,
            local_position: Vector2,
            zoom: float
        ):
        pygame.draw.circle(
            screen,
            POSITION_POINT_COLOR,
            local_position,
            POSITION_POINT_RADIUS * zoom
        )