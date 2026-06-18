import random

import pytest
from pygame.math import Vector2

from src.scenes.main.level.generator import (
    GENERATOR_TEMPLATE_LEVEL,
    LevelGenerator,
    PerlinNoise,
)
from src.scenes.main.level.loader import LevelLoader, RawLevel
from src.scenes.main.level.saver import LevelSaver


@pytest.fixture
def size():
    return (10, 10)

@pytest.fixture
def path_length():
    return 15

@pytest.fixture
def seed1():
    return 55


def test_generator_init(path_length, size, seed1):
    random.seed(seed1)
    level_loader = LevelLoader()
    ll = LevelGenerator(level_loader, True)
    template, heights = ll.get_template_and_heights()
    assert type(heights) is list
    assert type(template) is RawLevel
    tiles = ll.generate(path_length, size).tiles
    print(f"Generated Tiles: {tiles}")
    LevelSaver().save_map(tiles, GENERATOR_TEMPLATE_LEVEL)

def test_perlin_noise():
    PerlinNoise().noise2d(1.5, 1.2)
    assert PerlinNoise().noise2d(2, 2) == 0