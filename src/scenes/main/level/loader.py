import json
from dataclasses import dataclass
from pathlib import Path

import pygame

from src.core.singletones.image_loader import image_loader as il


@dataclass
class RawLevel:
    # Сырая карта тайлов
    tiles: list[list[int]]
    # Неразделённый тайлсет.
    tileset: pygame.Surface
    metadata: dict


class LevelLoader:
    """Загрузчик метаданных уровня, тайлсета и карты тайлов."""

    LEVELS_FOLDER = "res/levels/"
    TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
    MAPS_FOLDER = LEVELS_FOLDER + "maps/"
    DEFAULT_LEVEL_NAME = "default"

    def load_data(self, level_name):
        try:
            with open(Path(self.LEVELS_FOLDER, f"{level_name}.json"), "r") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Не удалось загрузить уровень: {e}")

    def load_tileset(self, tileset_name):
        return il.load_image(
            Path(self.TILESET_FOLDER, tileset_name)
        ).surface

    def load_map(self, map_name):
        tiles = list()
        with open(Path(self.MAPS_FOLDER, map_name), "r") as f:
            for line in f.readlines():
                tiles.append(list(map(int, line.split(","))))
        return tiles

    def load_level(self, level_name):
        """Загружает уровень из папки уровней с соответствующим названием."""
        level_data = self.load_data(level_name)
        tileset = self.load_tileset(level_data["tileset_name"])
        tiles = list()
        if "map_name" in level_data:
            tiles = self.load_map(level_data["map_name"])
        return RawLevel(tiles=tiles, tileset=tileset, metadata=level_data)

    def load_template_level(self):
        """Подгрузка шаблона для генерации уровня."""
        return self.load_level(self.DEFAULT_LEVEL_NAME)