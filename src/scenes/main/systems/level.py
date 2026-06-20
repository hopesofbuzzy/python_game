from pygame.math import Vector2

from src.config.generator_config import *
from src.scenes.main.factories.map_factory import MapFactory

# Генерация уровня
from src.scenes.main.level.builder import Level, LevelBuilder
from src.scenes.main.level.generator import LevelGenerator
from src.scenes.main.level.loader import LevelLoader
from src.scenes.main.level.saver import LevelSaver

DEFAULT_LEVEL_NAME = "generator_template"

class LevelManager:
    """Менеджер генерации и загрузки уровня."""
    def __init__(self, add_object_func):
        self.add_object = add_object_func

    def generate_level(self):
        # Генерация уровня.
        raw_level = LevelGenerator(LevelLoader(), True).generate(
            PATH_LENGTH,
            SIZE,
            SEED,
            NOISE_AMPLITUDE,
            WAVE_AMOUNT
        )
        # Постройка
        level = LevelBuilder(
            LevelLoader(),
            MapFactory(self.add_object)
        ).build(
            Vector2(0, 0),
            raw_level
        )
        return level

    def load_existing_level(self, level_name: str):
        level_builder: LevelBuilder = LevelBuilder(
            LevelLoader(),
            MapFactory(self.add_object)
        )
        raw_level = level_builder.load(level_name)
        level = level_builder.build(Vector2(0, 0), raw_level)
        return level