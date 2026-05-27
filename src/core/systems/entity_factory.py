from src.core.systems.images import ImageLoader
from src.objects import *

class EntityFactory:
    """Фабрика сборки объектов сцены."""
    def __init__(self, scene, image_loader, cursor):
        # View инъекция (ImageLoader).
        self.il = image_loader
        # Controller инъекция.
        self.cursor = cursor
        self.scene = scene

    def create_plant(self, position, cls_model, cls_view):
        plant_model = cls_model(local_position=position)
        plant = GameObject(
            model=plant_model,
            view=cls_view(self.il),
        )
        self.scene.add_object(plant)
        return plant

    def create_enemy(self, cls_model, cls_view, position, path):
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

    def create_bullet(self, direction, position, damage):
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
        return bullet

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
        