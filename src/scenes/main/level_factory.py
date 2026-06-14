from src.core.objects import TileMapView
from src.scenes.main.game_map import (
    GameMap,
    GameMapModel,
    GameMapController
)


class LevelFactory:
    """Фабрика сборки объектов уровня (карта)."""

    def __init__(self, add_object, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        # Controller инъекция.
        self.cursor = cursor
        # Метод добавления объекта.
        self.add_object = add_object

    def create_gamemap(self, position, tiles, tileset):
        tilemap_model = GameMapModel(local_position=position, tiles=tiles)
        tilemap_view = TileMapView(il=self.il, tileset=tileset)
        tilemap = GameMap(
            model=tilemap_model,
            view=tilemap_view,
            controller=GameMapController(tilemap_model, self.cursor),
        )
        self.add_object(tilemap)
        return tilemap
