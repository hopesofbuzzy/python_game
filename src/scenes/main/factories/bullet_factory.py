import logging
from pygame.math import Vector2

from src.scenes.main.objects.plants import Bullet, BulletModel, BulletView

class BulletFactory:
    """Фабрика сборки пули растения."""

    def __init__(self, add_object, image_loader):
        # View инъекция (ImageLoader).
        self.il = image_loader
        self.add_object = add_object

    def create_bullet(self, direction, position, attack):
        bullet_model = BulletModel(local_position=position, attack=attack)
        bullet_model.set_velocity(direction.x, direction.y)
        bullet = Bullet(model=bullet_model, view=BulletView(self.il))
        self.add_object(bullet)
        return bullet