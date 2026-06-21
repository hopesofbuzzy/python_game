import logging

from src.config.plants import PLANT_DATA


class MapLevelDataComponent:
    def __init__(self):
        self.plants: set[tuple] = set()
        self.poses_to_place: set = set()
        self.path_poses = set()
        self.start_pos = tuple()
        self.end_pos = tuple()

    def is_position_to_place_plant(
        self, plant_name: str, position: tuple
    ) -> bool:
        logging.debug(f"Проверка посадки: {plant_name}")
        if PLANT_DATA[plant_name]["road_spawn"]:
            return tuple(position) in self.path_poses
        else:
            return tuple(position) in self.poses_to_place
        # if plant_name in self.poses_to_place.keys():
        #     return tuple(position) in self.poses_to_place[plant_name]
        # else:
        #     return tuple(position) in self.poses_to_place["_"]

    def is_position_free(self, position: tuple) -> bool:
        return tuple(position) not in self.plants

    def add_plant(self, tile_pos, plant=None):
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
                if tile_idx in tiles_to_place:
                    self.poses_to_place.add((x, y))
        if (
            self.start_pos == tuple()
            or self.end_pos == tuple()
            or len(self.path_poses) == 0
            or len(self.poses_to_place) == 0
        ):
            logging.debug(f"GameMap (Parsed): {self}")
            raise Exception(
                "Не удалось распарсить карту, не найденые нужные сущности."
            )
