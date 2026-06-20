from src.scenes.main.objects.bullet import Bullet

class BulletController:
    def __init__(self):
        ...

    def remove_bullet(self, bullet: Bullet):
        bullet.free()