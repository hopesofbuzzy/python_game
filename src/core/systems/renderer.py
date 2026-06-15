import pygame

from src.core.objects import (
    PositionComponent,
    Camera,
    Scene
)


class Renderer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Camera):
        screen.fill((0, 0, 0))
        for object in scene.object_registry.values():
                if object.has(PositionComponent):
                    object.draw(
                        screen,
                        camera.to_local(object.get(PositionComponent).position),
                        camera.zoom
                    )
