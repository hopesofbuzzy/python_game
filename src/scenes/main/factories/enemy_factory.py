import logging
from pygame.math import Vector2

from src.core.objects.game_object import View
from src.scenes.main.objects.enemy import Enemy
from src.scenes.main.objects.plants import Bullet, BulletModel, BulletView, Plant


class EnemyFactory:
    """
        Фабрика сборки объектов сцены

        Инъекции:
            add_object(...),
            image_loader: load_image(...),
            cursor: ...
    """

    def __init__(self, add_object, image_loader):
        # View инъекция (ImageLoader).
        self.il = image_loader
        self.add_object = add_object

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