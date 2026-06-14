from pygame.math import Vector2

from src.scenes.main.objects.enemy import Enemy
from src.scenes.main.objects.inventory import (
    Inventory,
    InventoryController,
    InventoryModel,
)
from src.scenes.main.objects.plants import Bullet, BulletModel, BulletView, Plant


class EntityFactory:
    """
        Фабрика сборки объектов сцены

        Инъекции:
            add_object(...),
            image_loader: load_image(...),
            cursor: ...
    """

    def __init__(self, add_object, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        # Controller инъекция.
        self.cursor = cursor
        self.add_object = add_object

    def create_plant(self, position, tile_pos, cls_model, cls_view):
        plant_model = cls_model(local_position=position, tile_pos=tile_pos)
        plant = Plant(
            model=plant_model,
            view=cls_view(self.il),
        )
        self.add_object(plant)
        return plant

    def create_enemy(self, cls_model, cls_view, position, path):
        enemy_model = cls_model(local_position=position, path=path)
        enemy = Enemy(model=enemy_model, view=cls_view(self.il))
        self.add_object(enemy)
        return enemy

    def create_bullet(self, direction, position, attack):
        bullet_model = BulletModel(local_position=position, attack=attack)
        bullet_model.set_velocity(direction.x, direction.y)
        bullet = Bullet(model=bullet_model, view=BulletView(self.il))
        self.add_object(bullet)
        return bullet

    def create_inventory(self):
        model = InventoryModel(local_position=Vector2(0, 0))
        inventory = Inventory(
            model=model, controller=InventoryController(model, self.cursor)
        )
        self.add_object(inventory)
        return inventory
