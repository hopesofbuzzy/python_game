import pygame

from src.core.systems.camera import Camera
from src.core.systems.scene import Scene


class Renderer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Camera):
        screen.fill((0, 0, 0))
        for object in scene.object_registry.values():
            if object.view:
                object.view.draw(
                    screen, object.model, camera.to_local(object.model.position)
                )
