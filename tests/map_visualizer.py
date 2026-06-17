import logging
import pygame
from pygame.math import Vector2

from src.main import main
from src.core.objects.scene import Scene

# Фабрики и строители.
from src.scenes.main.factories.map_factory import MapFactory
from src.scenes.main.level.builder import Level, LevelBuilder
from src.scenes.main.level.loader import LevelLoader


LEVEL_NAME = "default"

class MapScene(Scene):
    def ready(self):
        self.setup_level()

    def setup_level(self):
        LevelBuilder(
            LevelLoader(),
            MapFactory(self.add_object)
        ).load_and_create_level(
            Vector2(0, 0),
            LEVEL_NAME,
            False,
            False
        )

DEBUG = False

if __name__ == "__main__":
    main(MapScene)
