import pytest
import random
from pygame.math import Vector2

from src.scenes.main.level.generator import LevelGenerator, WFC, GENERATOR_TEMPLATE_LEVEL
from src.scenes.main.level.loader import LevelLoader, RawLevel
from src.scenes.main.level.saver import LevelSaver


@pytest.fixture
def size():
    return (10, 10)

@pytest.fixture
def seed1():
    return 55


@pytest.fixture
def rules():
    ll = LevelGenerator(LevelLoader(), True)
    template, rules = ll.get_template_and_rules()
    return rules

def test_generator_init(size, seed1):
    random.seed(seed1)
    level_loader = LevelLoader()
    ll = LevelGenerator(level_loader, True)
    template, rules = ll.get_template_and_rules()
    assert type(rules) is dict
    assert type(template) is RawLevel
    print(f"Loaded rules: {rules}")
    tiles = ll.generate(size).tiles
    print(f"Generated Tiles: {tiles}")
    LevelSaver().save_map(tiles, GENERATOR_TEMPLATE_LEVEL)

def test_wfc_inti(rules, size):
    wfc = WFC(rules, size)
    assert type(wfc.rules) is dict
    assert type(wfc.size) is tuple