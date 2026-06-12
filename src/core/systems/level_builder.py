from dataclasses import dataclass, field

import pygame

from src.core.objects import GameObject
from src.core.systems.level_factory import LevelFactory
from src.core.systems.level_loader import LevelLoader


@dataclass
class ParsedMap:
    start_pos: tuple = field(default_factory=tuple)
    end_pos: tuple = field(default_factory=tuple)
    path_poses: set[tuple] = field(default_factory=set)
    poses_to_place: set[tuple] = field(default_factory=set)

@dataclass
class Level:
    tilemap: GameObject
    path: list
    parsed_map: ParsedMap

class LevelBuilder:
    """Центральный оркестратор строительства уровня."""
    def __init__(self, scene, image_loader, cursor):
        # Загрузчик уровней.
        self.lm = LevelLoader(image_loader)
        # Фабрика уровней.
        self.lf = LevelFactory(scene, image_loader, cursor)

    def load_and_create_level(self, position, level_name) -> Level:
        raw_level = self.lm.load_level(level_name)
        tileset = self.split_tileset(raw_level.tileset, raw_level.metadata["tile_size"])
        tilemap = self.lf.create_tilemap(position, raw_level.tiles, tileset)
        parsed_map = self.parse_map(
            tilemap,
            raw_level.metadata["start_tile"],
            raw_level.metadata["end_tile"],
            raw_level.metadata["path_tiles"],
            raw_level.metadata["tiles_to_place"]
        )
        path = self.build_pathes(tilemap, parsed_map)
        return Level(
            tilemap,
            path,
            parsed_map
        )

    def parse_map(
            self,
            tilemap,
            start_tile,
            end_tile,
            path_tiles,
            tiles_to_place
    ) -> ParsedMap:
        """Парсит карту, извлекая сущности по idx тайлов из тайлсета."""
        parsed_map = ParsedMap()
        for ridx, row in enumerate(tilemap.model.tiles):
            for cidx, tile_idx in enumerate(row):
                x = cidx  # * tile_size
                y = ridx  # * tile_size
                if tile_idx == start_tile:
                    parsed_map.start_pos = (x, y)
                elif tile_idx == end_tile:
                    parsed_map.end_pos = (x, y)
                elif tile_idx in path_tiles:
                    parsed_map.path_poses.add((x, y))
                elif tile_idx in tiles_to_place:
                    parsed_map.poses_to_place.add((x, y))
        if (
            parsed_map.start_pos == tuple()
            or parsed_map.end_pos == tuple()
            or len(parsed_map.path_poses) == 0
            or len(parsed_map.poses_to_place) == 0
        ):
            print(parsed_map)
            raise Exception("Не удалось распарсить карту, не найденые нужные сущности.") 
        return parsed_map

    def build_pathes(self, tilemap, parsed_map: ParsedMap) -> list:
        """
            Строит путь для врагов по тайлам карты.
            Путь может разветвляться для более интересного тавер дефенса,
            поэтому мы будем хранить карту возможных направлений движения для врага.
        """
        queue = [parsed_map.start_pos,]
        visited = set()
        for tile_pos in queue:
            for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_tile_pos = (tile_pos[0] + direction[0], tile_pos[1] + direction[1])
                if (new_tile_pos in parsed_map.path_poses or new_tile_pos == parsed_map.end_pos) and new_tile_pos not in visited:
                    queue.append(new_tile_pos)
                    visited.add(new_tile_pos)
        return queue

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