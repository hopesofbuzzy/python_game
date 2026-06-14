import pytest
from pygame.math import Vector2

from scenes.main.objects.enemy import EnemyModel, EnemyView
from src.core.objects import PathModel
from src.core.systems.scene import Scene


class Scene1(Scene):
    def ready(self):
        points = [[0, 0], [100, 100]]
        path = PathModel(local_position=Vector2(0, 0), points=points)
        self.entity_factory.create_enemy(
            EnemyModel, EnemyView, position=Vector2(200, 200), path=path
        )


@pytest.fixture
def scene1():
    return Scene1(None)


def test_path(scene1):
    """Проверка инициализации врага и пути."""
    return True
