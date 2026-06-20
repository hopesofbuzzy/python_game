import pygame

from src.core.objects import Camera, PositionComponent, Scene, UITransform


class Renderer:
    def draw(self, screen: pygame.Surface, scene: Scene, camera: Camera):
        screen.fill((0, 0, 0))
        for object in scene.z_index_object_registry:
                # Глоабльная отрисовка.
                if object.has(PositionComponent):
                    object.draw(
                        screen,
                        None,
                        camera.to_local(object.get(PositionComponent).position),
                        camera
                    )
                # Отрисовка интерфейса (зависит от флага anchor).
                elif object.has(UITransform):
                    position = None
                    if object.get(UITransform).anchor:
                        position = camera.to_local(object.get(UITransform).position)
                    else:
                        position = object.get(UITransform).position
                    object.draw(
                        screen,
                        object.get(UITransform).size,
                        position,
                        camera
                    )
