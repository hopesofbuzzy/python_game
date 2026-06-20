from src.scenes.main.objects import Enemy


class EnemyController:
    def __init__(self):
        ...

    def remove_enemy(self, enemy: Enemy):
        enemy.free()

    def attack_enemy(self, enemy: Enemy):
        ...