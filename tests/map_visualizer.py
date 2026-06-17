import logging
import random

import pygame
from pygame.math import Vector2

from src.core.objects.scene import Scene
from src.main import main

# Фабрики и строители.
from src.scenes.main.factories.map_factory import MapFactory
from src.scenes.main.level.builder import Level, LevelBuilder
from src.scenes.main.level.generator import LevelGenerator
from src.scenes.main.level.loader import LevelLoader
from src.scenes.main.level.saver import LevelSaver

LEVEL_NAME = "generator_template"
SEED = 66
SIZE = (20, 20)

class MapScene(Scene):
    """Небольшая сцена для визуализации карты."""
    def ready(self):
        self.setup_level()

    def setup_level(self):
        random.seed(SEED)
        level_loader = LevelLoader()
        ll = LevelGenerator(level_loader, True)
        template, rules = ll.get_template_and_rules()
        tiles = ll.generate(SIZE).tiles
        LevelSaver().save_map(tiles, LEVEL_NAME)
        LevelBuilder(
            LevelLoader(),
            MapFactory(self.add_object)
        ).load_and_create_level(
            Vector2(0, 0),
            LEVEL_NAME,
            False,
            False
        )

if __name__ == "__main__":
    main(MapScene)
