import json
from dataclasses import dataclass
from pathlib import Path

from src.core.singletones.image_loader import image_loader as il


class LevelSaver:
    """Сохранение (сгенерированного) уровня."""

    LEVELS_FOLDER = "res/levels/"
    TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
    MAPS_FOLDER = LEVELS_FOLDER + "maps/"

    def save_data(self, metadata: dict, level_name):
        ...

    def save_map(self, tiles: list, map_name):
        lines = list()
        for tile_line in tiles:
            lines.append(",".join(map(str, tile_line)))
        with open(Path(self.MAPS_FOLDER, f"{map_name}.csv"), "w") as f:
            for line in lines:
                f.write(line + "\n")
