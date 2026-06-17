import pytest
from pygame.math import Vector2

from src.scenes.main.level.generator import LevelGenerator
from src.scenes.main.level.loader import LevelLoader


@pytest.fixture
def raw_level():
    LevelLoader().load_template_level


def test_generator1(raw_level):
    """Проверка первичной генерации."""
    level_loader = LevelLoader()
    LevelGenerator(level_loader, True).generate()
    return True