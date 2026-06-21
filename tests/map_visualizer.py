from src.config.generator_config import *
from src.core.objects.scene import Scene

# Фабрики и строители.
from src.main import main
from src.scenes.main.level.generator import LevelGenerator
from src.scenes.main.level.loader import LevelLoader
from src.scenes.main.level.saver import LevelSaver

LEVEL_NAME = "generator_template"


class MapScene(Scene):
    """Небольшая сцена для визуализации карты."""

    def ready(self):
        self.setup_level()

    def setup_level(self):
        ll = LevelGenerator(LevelLoader(), True)
        raw_level = ll.generate(
            PATH_LENGTH, SIZE, seed, NOISE_AMPLITUDE, WAVE_AMOUNT
        )
        LevelSaver().save_level(raw_level, LEVEL_NAME)


if __name__ == "__main__":
    main(MapScene)
