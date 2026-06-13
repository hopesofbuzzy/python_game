import json
from dataclasses import dataclass
from pathlib import Path

import pygame


@dataclass
class RawLevel:
    tiles: list[list]
    tileset: pygame.Surface
    metadata: dict


class LevelLoader:
    """Загрузчик метаданных уровня, тайлсета и карты тайлов."""

    LEVELS_FOLDER = "res/levels/"
    TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
    MAPS_FOLDER = LEVELS_FOLDER + "maps/"

    def __init__(self, image_loader):
        self.il = image_loader

    def load_level(self, level_name: str):
        """Загружает уровень из папки уровней с соответствующим названием."""
        level_data = dict()
        # Подгрузка данных уровня.
        try:
            with open(Path(self.LEVELS_FOLDER, f"{level_name}.json"), "r") as f:
                level_data = json.load(f)
        except Exception as e:
            raise Exception(f"Не удалось загрузить уровень: {e}")
        # Подгрузка тайлсета уровня.
        tileset = self.il.load_image(
            Path(self.TILESET_FOLDER, level_data["tileset_name"])
        ).surface
        # Подгрузка карты.
        tiles = list()
        with open(Path(self.MAPS_FOLDER, level_data["map_name"]), "r") as f:
            for line in f.readlines():
                tiles.append(list(map(int, line.split(","))))
        return RawLevel(tiles=tiles, tileset=tileset, metadata=level_data)
