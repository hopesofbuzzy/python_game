import logging
from dataclasses import dataclass, field

from src.core.objects.game_object import GameObject
from src.core.objects.components.map import (
    Map,
    MapControllerComponent,
    MapModelComponent,
    MapViewComponent,
)


class MapLevelDataComponent:
    def __init__(self):
        self.plants: set[tuple] = set()
        self.poses_to_place = set()
        self.path_poses = set()
        self.start_pos = tuple()
        self.end_pos = tuple()

    def is_position_to_place_plant(self, position: tuple) -> bool:
        return tuple(position) in self.poses_to_place

    def is_position_to_place_road_plant(self, position: tuple) -> bool:
        return tuple(position) in self.path_poses

    def is_position_free(self, position: tuple) -> bool:
        return tuple(position) not in self.plants

    def add_plant(self, tile_pos):
        self.plants.add(tuple(tile_pos))

    def remove_plant(self, tile_pos):
        if tuple(tile_pos) in self.plants:
            self.plants.remove(tuple(tile_pos))

    def parse_map(
        self, tiles, start_tile, end_tile, path_tiles, tiles_to_place
    ):
        """Парсит карту, извлекая сущности по idx тайлов из тайлсета."""
        for ridx, row in enumerate(tiles):
            for cidx, tile_idx in enumerate(row):
                x = cidx  # * tile_size
                y = ridx  # * tile_size
                if tile_idx == start_tile:
                    self.start_pos = (x, y)
                elif tile_idx == end_tile:
                    self.end_pos = (x, y)
                elif tile_idx in path_tiles:
                    self.path_poses.add((x, y))
                elif tile_idx in tiles_to_place:
                    self.poses_to_place.add((x, y))
        if (
            self.start_pos == tuple()
            or self.end_pos == tuple()
            or len(self.path_poses) == 0
            or len(self.poses_to_place) == 0
        ):
            logging.debug(f"GameMap (Parsed): {self}")
            raise Exception("Не удалось распарсить карту, не найденые нужные сущности.")
