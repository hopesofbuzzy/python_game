import json
from dataclasses import dataclass
from pathlib import Path

import pygame

from src.core.singletones.image_loader import image_loader as il
from src.scenes.main.level.generator import GENERATOR_TEMPLATE_LEVEL


@dataclass
class RawLevel:
    # Сырая карта тайлов
    tiles: list[list[int]]
    # Неразделённый тайлсет.
    tileset: pygame.Surface
    metadata: dict

LEVELS_FOLDER = "res/levels/"
TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
MAPS_FOLDER = LEVELS_FOLDER + "maps/"

class LevelLoader:
    """Загрузчик метаданных уровня, тайлсета и карты тайлов."""

    def load_data(self, level_name):
        """Загрузка данных уровня."""
        try:
            with open(Path(LEVELS_FOLDER, f"{level_name}.json"), "r") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Не удалось загрузить уровень: {e}")

    def load_tileset(self, tileset_name):
        """Загрузка тайлсета уровня."""
        return il.load_image(
            str(Path(TILESET_FOLDER, tileset_name))
        ).surface

    def load_map(self, map_name):
        """Загрузка карты уровня."""
        tiles = list()
        with open(Path(MAPS_FOLDER, map_name), "r") as f:
            for line in f.readlines():
                tiles.append(list(map(int, line.split(","))))
        return tiles

    def load_level(self, level_name, load_map: bool = True):
        """Загружает уровень из папки уровней с соответствующим названием."""
        level_data = self.load_data(level_name)
        tileset = self.load_tileset(level_data["tileset_name"])
        tiles = list()
        if load_map and "map_name" in level_data:
            tiles = self.load_map(level_data["map_name"])
        return RawLevel(tiles=tiles, tileset=tileset, metadata=level_data)

    def load_generator_template_level(self):
        """Подгрузка шаблона для генерации уровня."""
        return self.load_level(GENERATOR_TEMPLATE_LEVEL, False)