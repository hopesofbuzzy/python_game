import logging
from dataclasses import dataclass, field

from src.core.objects.components.map import (
    Map,
    MapControllerComponent,
    MapModelComponent,
    MapViewComponent,
)
from src.core.objects.game_object import GameObject


class MapLevelDataComponent:
    def __init__(self):
        self.plants: set[tuple] = set()
        self.poses_to_place: dict[str, set] = dict()
        self.path_poses = set()
        self.start_pos = tuple()
        self.end_pos = tuple()

    def is_position_to_place_plant(self, plant_name: str, position: tuple) -> bool:
        logging.debug(f"Проверка посадки: {plant_name}")
        logging.debug(f"{self.poses_to_place.keys()}")
        if plant_name in self.poses_to_place.keys():
            return tuple(position) in self.poses_to_place[plant_name]
        else:
            return tuple(position) in self.poses_to_place["_"]

    def is_position_free(self, position: tuple) -> bool:
        return tuple(position) not in self.plants

    def add_plant(self, tile_pos, plant = None):
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
                for plant_name, plant_tiles_to_place in tiles_to_place.items():
                    if tile_idx in plant_tiles_to_place:
                        self.poses_to_place[plant_name] = (
                            self.poses_to_place.setdefault(plant_name, set())
                        )
                        self.poses_to_place[plant_name].add((x, y))
        if (
            self.start_pos == tuple()
            or self.end_pos == tuple()
            or len(self.path_poses) == 0
            or len(self.poses_to_place) == 0
        ):
            logging.debug(f"GameMap (Parsed): {self}")
            raise Exception("Не удалось распарсить карту, не найденые нужные сущности.")