import pygame

from src.core.objects import (
    PositionComponent,
    UITransform,
    Camera,
    Scene
)


class Renderer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Camera):
        screen.fill((0, 0, 0))
        for object in scene.object_registry.values():
                # Глоабльная отрисовка.
                if object.has(PositionComponent):
                    object.draw(
                        screen,
                        camera.to_local(object.get(PositionComponent).position),
                        camera.zoom
                    )
                # Отрисовка интерфейса (зависит от флага screen_anchor).
                elif object.has(UITransform):
                    position = None
                    if object.get(UITransform).screen_anchor:
                        position = object.get(UITransform).position
                    else:
                        position = camera.to_local(object.get(UITransform).position)
                    object.draw(
                        screen,
                        position,
                        camera.zoom
                    )
