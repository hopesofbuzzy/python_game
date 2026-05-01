import pygame

from src.core.objects.game_object import GameObject
from src.core.systems.scene import Scene

class Renderer:
    def draw(
        self,
        screen: pygame.Surface,
        scene: Scene
    ):
        for object in scene.object_registry.values():
            object.view.draw(screen, object.model)