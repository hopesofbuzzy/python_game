import logging
from dataclasses import dataclass, field

import pygame

from src.core.objects.components.map import Map, MapModelComponent
from src.scenes.main.factories.map_factory import MapFactory
from src.scenes.main.level.loader import LevelLoader
from src.scenes.main.objects.components.map_level_data import MapLevelDataComponent
from src.scenes.main.systems.waves import ParsedWaves, Wave, WaveObject


@dataclass
class Level:
    map: Map
    path: list
    parsed_waves: ParsedWaves

DEFAULT_LEVEL_NAME = "default"

class LevelBuilder:
    """Центр загрузки и строительства уровня."""

    def __init__(
        self,
        level_loader: LevelLoader,
        level_factory: MapFactory
    ):
        # Загрузчик уровней.
        self.lm = level_loader
        # Фабрика уровней.
        self.lf = level_factory

    def load_and_create_level(
            self,
            position,
            level_name: str = DEFAULT_LEVEL_NAME,
            parse_map: bool = True,
            parse_waves: bool = True
    ) -> Level:
        """Загружает и строит уровень: карта, пути, волны."""
        raw_level = self.lm.load_level(level_name)
        tileset = self.split_tileset(raw_level.tileset, raw_level.metadata["tile_size"])
        map = self.lf.create_map(position, raw_level.tiles, tileset)
        path = list()
        if parse_map:
            map.get(MapLevelDataComponent).parse_map(
                map.get(MapModelComponent).tiles,
                raw_level.metadata["start_tile"],
                raw_level.metadata["end_tile"],
                raw_level.metadata["path_tiles"],
                raw_level.metadata["tiles_to_place"]
            )
            path = self.build_pathes(map)
        parsed_waves = ParsedWaves(list())
        if parse_waves:
            parsed_waves = self.parse_waves(raw_level.metadata)
        return Level(map, path, parsed_waves)

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

    def build_pathes(self, gamemap: Map) -> list:
        """
        Строит путь для врагов по тайлам карты.
        Путь может разветвляться для более интересного тавер дефенса,
        поэтому мы будем хранить карту возможных направлений движения для врага.
        """
        map_level_data = gamemap.get(MapLevelDataComponent)
        queue = [
            map_level_data.start_pos,
        ]
        visited = set()
        
        for tile_pos in queue:
            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_tile_pos = (tile_pos[0] + direction[0], tile_pos[1] + direction[1])
                if (
                    new_tile_pos in map_level_data.path_poses
                    or new_tile_pos == map_level_data.end_pos
                ) and new_tile_pos not in visited:
                    queue.append(new_tile_pos)
                    visited.add(new_tile_pos)
        # logging.debug(f"{queue}")
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
