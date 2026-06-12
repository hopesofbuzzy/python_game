from src.objects import GameObject, TileMapController, TileMapModel, TileMapView


class LevelFactory:
    """Фабрика сборки объектов уровня (карта)."""
    def __init__(self, scene, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        # Controller инъекция.
        self.cursor = cursor
        # Сцена для доабвления объектов.
        self.scene = scene

    def create_tilemap(self, position, tiles, tileset):
        tilemap_model = TileMapModel(
            local_position=position,
            tiles=tiles
        )
        tilemap_view=TileMapView(
            il=self.il,
            tileset=tileset
        )
        tilemap = GameObject(
            model=tilemap_model,
            view=tilemap_view,
            controller=TileMapController(tilemap_model, self.cursor)
        )
        self.scene.add_object(tilemap)
        return tilemap