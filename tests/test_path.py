import pytest
from pygame.math import Vector2

from src.core.objects import PathModel
from src.core.systems.scene import Scene
from src.objects.enemy import EnemyModel, EnemyView


class Scene1(Scene):
    def ready(self):
        points = [[0, 0], [100, 100]]
        path = PathModel(local_position=Vector2(0, 0), points=points)
        enemy = self.entity_factory.create_enemy(
            EnemyModel, EnemyView, position=Vector2(200, 200), path=path
        )
        print(enemy)


@pytest.fixture
def scene1():
    return Scene1(None)


def test_path(scene1):
    """Проверка инициализации врага и пути."""
    return True
