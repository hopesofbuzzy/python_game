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


@pytest.fixture
def rules():
    ll = LevelGenerator(LevelLoader(), True)
    template, rules = ll.get_template_and_rules()
    return rules

def test_generator_init(path_length, size, seed1):
    random.seed(seed1)
    level_loader = LevelLoader()
    ll = LevelGenerator(level_loader, True)
    template, rules = ll.get_template_and_rules()
    assert type(rules) is dict
    assert type(template) is RawLevel
    print(f"Loaded rules: {rules}")
    tiles = ll.generate(path_length, size).tiles
    print(f"Generated Tiles: {tiles}")
    LevelSaver().save_map(tiles, GENERATOR_TEMPLATE_LEVEL)

# def test_wfc_init(rules, size):
#     wfc = WFC(rules, size)
#     assert type(wfc.rules) is dict
#     assert type(wfc.size) is tuple

def test_perlin_noise():
    PerlinNoise().noise2d(1.5, 1.2)
    assert PerlinNoise().noise2d(2, 2) == 0