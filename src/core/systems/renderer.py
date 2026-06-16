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
        for object in sorted(list(scene.object_registry.values()), key=lambda x: x.z_index):
                # Глоабльная отрисовка.
                if object.has(PositionComponent):
                    object.draw(
                        screen,
                        None,
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
                        object.get(UITransform).size,
                        position,
                        camera.zoom
                    )
