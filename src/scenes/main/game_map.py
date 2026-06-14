import logging
from dataclasses import dataclass, field

from src.core.objects.tile_map import (
    TileMap,
    TileMapModel,
    TileMapView,
    TileMapController
)

from src.core.objects.game_object import GameObject

@dataclass
class GameMapModel(TileMapModel):
    """
        Карта с игровой логикой и метаданными (SRP).

        Args:
            plants: список координат, занятых растениями.
            poses_to_place: позиции для посадки.
            path_poses: позиции дорог.
    """
    plants: set[tuple] = field(default_factory=set)
    poses_to_place: set[tuple] = field(default_factory=set)
    path_poses: set[tuple] = field(default_factory=set)
    start_pos: tuple = field(default_factory=tuple)
    end_pos: tuple = field(default_factory=tuple)

    def is_position_to_place_plant(self, position: tuple) -> bool:
        return position in self.poses_to_place

    def is_position_to_place_road_plant(self, position: tuple) -> bool:
        return position in self.path_poses

    def is_position_free(self, position: tuple) -> bool:
        return position not in self.plants

    def add_plant(self, plant, tile_pos):
        self.plants.add(tile_pos)

    def parse_map(
        self, start_tile, end_tile, path_tiles, tiles_to_place
    ):
        """Парсит карту, извлекая сущности по idx тайлов из тайлсета."""
        for ridx, row in enumerate(self.tiles):
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

@dataclass
class GameMapController(TileMapController):

    def add_plant(self, plant, tile_pos):
        self.model.add_plant(plant, tile_pos)

@dataclass
class GameMap(GameObject[GameMapModel, TileMapView, GameMapController]):
    ...