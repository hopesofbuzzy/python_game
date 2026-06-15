from src.core.objects import (
    Map,
    MapModelComponent,
    MapControllerComponent,
    MapViewComponent,
    PositionComponent
)
from src.scenes.main.objects import MapLevelDataComponent


class LevelFactory:
    """Фабрика сборки объектов уровня (карта)."""

    def __init__(self, add_object):
        # Метод добавления объекта.
        self.add_object = add_object

    def create_map(self, position, tiles, tileset):
        map_model_component = MapModelComponent(tiles)
        map = (
            Map()
            .add(PositionComponent(position, None))
            .add(map_model_component)
            .add(MapControllerComponent(map_model_component))
            .add(MapViewComponent(map_model_component, tileset))
            .add(MapLevelDataComponent())
        )
        self.add_object(map)
        return map
