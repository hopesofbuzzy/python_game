from src.core.systems.images import ImageLoader
from src.objects import *
from src.core.systems.level import LevelManager, Level

class EntityFactory:
    """
        Универсальная фабрика сборки объектов с доступом
        к сцене, загрузчику изображений и курсору для контроллера.
    """
    def __init__(self, scene, cursor):
        # View инъекция (ImageLoader).
        self.il = scene.il
        # Controller инъекция.
        self.cursor = cursor
        self.scene = scene
        # Для фабрики уровней (LevelManager).
        self.lm = LevelManager(self.il)

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
            local_position=position,
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

    def create_level(self, position, level_name):
        level = self.lm.load_level(level_name)
        tilemap_model = TileMapModel(
            local_position=position,
            tiles=level.tiles
        )
        tilemap_view=TileMapView(
            il=self.il,
            tileset=level.tileset
        )
        tilemap = GameObject(
            model=tilemap_model,
            view=tilemap_view,
            controller=TileMapController(tilemap_model, self.cursor)
        )
        self.scene.add_object(tilemap)
        return tilemap, level

    def create_inventory(self):
        model = InventoryModel(
            local_position=Vector2(0, 0)
        )
        inventory = GameObject(
            model=model,
            controller=InventoryController(model, self.cursor)
        )
        self.scene.add_object(inventory)
        return inventory
        