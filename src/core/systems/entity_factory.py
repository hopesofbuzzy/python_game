from src.core.systems.images import ImageLoader
from src.objects import *

class EntityFactory:
    """
        Универсальная фабрика сборки объектов с доступом
        к сцене, загрузчику изображений и курсору для контроллера.
    """
    def __init__(self, scene, cursor):
        self.il = ImageLoader()
        self.cursor = cursor
        self.scene = scene

    def create_plant(self, position):
        plant_model = MushroomModel(local_position=position)
        plant = GameObject(
            model=plant_model,
            view=MushroomView(self.il),
        )
        self.scene.add_object(plant)
        return plant

    def create_enemy(self, cls_model, cls_view, position, path):
        print(cls_model)
        enemy_model = cls_model(
            local_position=position,
            path=path
        )
        enemy = GameObject(
            model=enemy_model,
            view=cls_view(self.il)
        )
        self.scene.add_object(enemy)
        return enemy

    def create_bullet(self, direction, position, owner, damage):
        bullet_model = BulletModel(
            local_position=position.copy(),
            damage=damage
        )
        bullet_model.set_velocity(direction.x, direction.y)
        bullet = GameObject(
            model=bullet_model,
            view=BulletView(self.il)
        )
        self.scene.add_object(bullet)
        # print(self.scene.object_registry)
        owner.cooldown = True
        return bullet

    def create_tilemap(self, position, tiles_path, tileset_path):
        tilemap_model = TileMapModel(
            local_position=position
        )
        tilemap_view=TileMapView(
            il=self.il
        )
        # Загружаем уровень.
        with open(tiles_path, "r") as f:
            for line in f.readlines():
                tilemap_model._tiles.append(list(map(int, line.split(","))))
        # Делим tileset, извлекая наши тайлы.
        surface = self.il.load_image(tileset_path).surface
        if surface:
            tileset_size = surface.get_size()
            original_tile_size = tilemap_model.original_tile_size
            tile_size = tilemap_model.tile_size
            tile_idx = 0
            for row in range(0, tileset_size[1], original_tile_size):
                for col in range(0, tileset_size[0], original_tile_size):
                    tile = surface.subsurface(
                        pygame.Rect(
                            (col, row), (
                                original_tile_size,
                                original_tile_size
                            )
                        )
                    )
                    tile = pygame.transform.scale(
                        tile,
                        size=(tile_size, tile_size)
                    )
                    tilemap_view._tileset[tile_idx] = tile
                    tile_idx += 1
        tilemap = GameObject(
            model=tilemap_model,
            view=tilemap_view,
            controller=TileMapController(tilemap_model, self.cursor)
        )
        self.scene.add_object(tilemap)
        return tilemap