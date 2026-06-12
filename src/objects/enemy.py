from dataclasses import dataclass, field

from pygame.math import Vector2

from src.core.objects import CollisionShape, PathBodyModel, RectShape, RectView

ENEMY_SPEED = 35
ENEMY_HEALTH = 100
ENEMY_SIZE = Vector2(40, 40)
ENEMY_COLOR = (255, 25, 25)

# FastEnemy
FAST_ENEMY_COLOR = (80, 80, 255)
FAST_ENEMY_HEALTH = 40
FAST_ENEMY_SPEED = 60
FAST_ENEMY_SIZE = Vector2(30, 30)

@dataclass
class EnemyModel(PathBodyModel):
    shape: CollisionShape = field(default_factory=lambda: RectShape(size=ENEMY_SIZE))
    speed: float = field(default_factory=lambda: ENEMY_SPEED)
    health: int = ENEMY_HEALTH

    def handle_collision(self, other):
        ...

    def damage(self, damage: int):
        print(damage)
        self.health -= damage
        if self.health <= 0:
            self.free()

@dataclass
class EnemyView(RectView):
    color: tuple = ENEMY_COLOR
    size: Vector2 = field(default_factory=lambda: ENEMY_SIZE)


@dataclass
class FastEnemyModel(EnemyModel):
    speed: float = FAST_ENEMY_SPEED
    health: int = FAST_ENEMY_HEALTH

@dataclass
class FastEnemyView(EnemyView):
    color: tuple = FAST_ENEMY_COLOR
    size: Vector2 = field(default_factory=lambda: FAST_ENEMY_SIZE)