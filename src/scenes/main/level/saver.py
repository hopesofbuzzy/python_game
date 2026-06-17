import json
from dataclasses import dataclass
from pathlib import Path

import pygame

from src.core.singletones.image_loader import image_loader as il


@dataclass
class RawLevel:
    tiles: list[list]
    tileset: pygame.Surface
    metadata: dict


class LevelSaver:
    """Сохранение (сгенерированного) уровня."""

    LEVELS_FOLDER = "res/levels/"
    TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
    MAPS_FOLDER = LEVELS_FOLDER + "maps/"
    DEFAULT_LEVEL_NAME = "default"

    def save_data(self, metadata: dict, level_name: str = "generated"):
        ...
        # try:
        #     with open(Path(self.LEVELS_FOLDER, f"{level_name}.json"), "r") as f:
        #         return json.load(f)
        # except Exception as e:
        #     raise Exception(f"Не удалось загрузить уровень: {e}")

    def save_map(self, tiles: list, map_name: str = "generated"):
        ...
        # tiles = list()
        # with open(Path(self.MAPS_FOLDER, map_name), "r") as f:
        #     for line in f.readlines():
        #         tiles.append(list(map(int, line.split(","))))
        # return tiles
