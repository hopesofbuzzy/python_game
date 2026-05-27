from dataclasses import dataclass
import pygame

from src.core.systems.level_loader import LevelLoader
from src.core.systems.level_factory import LevelFactory
from src.core.objects import GameObject

@dataclass
class Level:
    tilemap: GameObject
    pathes: list[list]
    metadata: dict

class LevelBuilder:
    """Центральный оркестратор строительства уровня."""
    def __init__(self, scene, image_loader, cursor):
        # Загрузчик уровней.
        self.lm = LevelLoader(image_loader)
        # Фабрика уровней.
        self.lf = LevelFactory(scene, image_loader, cursor)

    def load_and_create_level(self, position, level_name):
        raw_level = self.lm.load_level(level_name)
        tileset = self.split_tileset(raw_level.tileset, raw_level.metadata["tile_size"])
        tilemap = self.lf.create_tilemap(position, raw_level.tiles, tileset)
        return Level(
            tilemap,
            [],
            raw_level.metadata
        )

    def build_pathes(self, tilemap, start_tile, path_tiles):
        """
            Строит объект пути для врагов по тайлам карты.
            Путь может разветвляться для более интересного тавер дефенса.
            (Yen's K-shortest).
        """
        ...

    def split_tileset(
            self,
            surface: pygame.Surface,
            tile_size: int
    ) -> dict[int, pygame.Surface]:
        """Деление изображения тайлсета на тайлы."""
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