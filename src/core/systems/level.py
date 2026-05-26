from dataclasses import dataclass, field
from pathlib import Path
import json
import pygame


@dataclass
class Level:
    tiles: list[list]
    tileset: dict[int, pygame.Surface]
    metadata: dict

class LevelManager:
    LEVELS_FOLDER = "res/levels"
    TILESET_FOLDER = "res/levels/tilesets"
    MAPS_FOLDER = "res/levels/maps"

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
        tileset_surface = self.il.load_image(
            Path(self.TILESET_FOLDER, level_data["tileset_name"])
        ).surface
        # Разделение тайлсета (без сжатия).
        tileset = self.split_tileset(tileset_surface, level_data["tile_size"])
        # Подгрузка карты.
        tiles = list()
        with open(Path(self.MAPS_FOLDER, level_data["map_name"]), "r") as f:
            for line in f.readlines():
                tiles.append(list(map(int, line.split(","))))
        return Level(
            tiles=tiles,
            tileset=tileset,
            metadata=level_data
        )

    def split_tileset(
            self,
            surface: pygame.Surface,
            tile_size: int
    ) -> dict[int, pygame.Surface]:
        tileset = dict()
        if surface:
            tileset_size = surface.get_size()
            tile_idx = 0
            for row in range(0, tileset_size[1], tile_size):
                for col in range(0, tileset_size[0], tile_size):
                    tile = surface.subsurface(
                        pygame.Rect(
                            (col, row), (
                                tile_size,
                                tile_size
                            )
                        )
                    )
                    tileset[tile_idx] = tile
                    tile_idx += 1
        return tileset