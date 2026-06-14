import logging
from dataclasses import dataclass, field

import pygame

from src.scenes.main.game_map import GameMap
from src.scenes.main.level_factory import LevelFactory
from src.scenes.main.level_loader import LevelLoader
from src.scenes.main.wave_manager import ParsedWaves, Wave, WaveObject


@dataclass
class Level:
    gamemap: GameMap
    path: list
    parsed_waves: ParsedWaves


class LevelBuilder:
    """
        Центр строительства уровня.

        Инъекции:
            add_object(...),
            image_loader: load_image(...),
            cursor: ...
    """

    def __init__(self, add_object, image_loader, cursor):
        # Загрузчик уровней.
        self.lm = LevelLoader(image_loader)
        # Фабрика уровней.
        self.lf = LevelFactory(add_object, image_loader, cursor)

    def load_and_create_level(self, position, level_name) -> Level:
        raw_level = self.lm.load_level(level_name)
        tileset = self.split_tileset(raw_level.tileset, raw_level.metadata["tile_size"])
        gamemap = self.lf.create_gamemap(position, raw_level.tiles, tileset)
        gamemap.model.parse_map(
            raw_level.metadata["start_tile"],
            raw_level.metadata["end_tile"],
            raw_level.metadata["path_tiles"],
            raw_level.metadata["tiles_to_place"]
        )
        parsed_waves = self.parse_waves(raw_level.metadata)
        path = self.build_pathes(gamemap)
        return Level(gamemap, path, parsed_waves)

    def parse_waves(self, metadata: dict):
        waves: list[dict] = metadata["waves"]
        parsed_waves = list()
        for wave_dict in waves:
            wave = Wave(wave_dict["timestamp"], list())
            enemy_amount_pairs = list(
                zip(wave_dict["enemy_type"], wave_dict["enemy_amount"])
            )
            for enemy, amount in enemy_amount_pairs:
                wave.wave_objects.append(WaveObject(enemy, amount))
            parsed_waves.append(wave)
        return ParsedWaves(parsed_waves)

    def build_pathes(self, gamemap) -> list:
        """
        Строит путь для врагов по тайлам карты.
        Путь может разветвляться для более интересного тавер дефенса,
        поэтому мы будем хранить карту возможных направлений движения для врага.
        """
        queue = [
            gamemap.model.start_pos,
        ]
        visited = set()
        
        for tile_pos in queue:
            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_tile_pos = (tile_pos[0] + direction[0], tile_pos[1] + direction[1])
                if (
                    new_tile_pos in gamemap.model.path_poses
                    or new_tile_pos == gamemap.model.end_pos
                ) and new_tile_pos not in visited:
                    queue.append(new_tile_pos)
                    visited.add(new_tile_pos)
        logging.debug(f"{queue}")
        return queue

    def split_tileset(
        self, surface: pygame.Surface, tile_size: int
    ) -> dict[int, pygame.Surface]:
        """Деление изображения тайлсета на тайлы."""
        tileset = dict()
        if surface:
            tileset_size = surface.get_size()
            tile_idx = 0
            for row in range(0, tileset_size[1], tile_size):
                for col in range(0, tileset_size[0], tile_size):
                    tile = surface.subsurface(
                        pygame.Rect((col, row), (tile_size, tile_size))
                    )
                    tileset[tile_idx] = tile
                    tile_idx += 1
        return tileset
