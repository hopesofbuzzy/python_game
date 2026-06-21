from pygame.math import Vector2

from src.core.objects import (
    Map,
    MapControllerComponent,
    MapModelComponent,
    MapViewComponent,
    PositionComponent,
)
from src.scenes.main.objects import MapLevelDataComponent

DEFAULT_MAP_POSITION = Vector2(0, 0)

class MapFactory:
    """Фабрика сборки объектов уровня (карта)."""

    def __init__(self, add_object):
        # Метод добавления объекта.
        self.add_object = add_object

    def create_map(self, tiles, tileset):
        map_model_component = MapModelComponent(tiles)
        map = (
            Map()
            .add(PositionComponent(DEFAULT_MAP_POSITION, None))
            .add(map_model_component)
            .add(MapControllerComponent(map_model_component))
            .add(MapViewComponent(map_model_component, tileset))
            .add(MapLevelDataComponent())
        )
        self.add_object(map)
        return map
