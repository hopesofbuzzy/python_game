from dataclasses import dataclass, field

import pygame
from pygame.event import Event
from pygame.math import Vector2

from src.core.objects import *
from src.core.systems.event import Event


@dataclass
class TileMapView(View):
    _scaled_tilesets: dict[float, dict[int, pygame.Surface]] = field(default_factory=dict)
    tileset: dict[int, pygame.Surface] = field(default_factory=dict)
    tile_size: int = 50

    def get_scaled_tileset(self, size: float):
        if size not in self._scaled_tilesets.keys():
            self._scaled_tilesets[size] = dict()
            for tile_idx, tile in self.tileset.items():
                overall_size = (self.tile_size * size, self.tile_size * size)
                tile = pygame.transform.scale(tile, size=overall_size)
                self._scaled_tilesets[size][tile_idx] = tile
        return self._scaled_tilesets[size]

    def draw(self, screen: pygame.Surface, model, local_position, zoom):
        pos = local_position
        scaled_tileset = self.get_scaled_tileset(zoom)
        for ridx, row in enumerate(model.tiles):
            for cidx, tile_idx in enumerate(row):
                tile = scaled_tileset[tile_idx]
                screen.blit(
                    tile,
                    dest=(
                        pos.x + cidx * model.tile_size * zoom,
                        pos.y + ridx * model.tile_size * zoom,
                    ),
                )


@dataclass
class TileMapModel(Model):
    """
    Модель карты тайлов.

    Args:
        tiles (list[list[int]]): подгруженная карта.
        tileset (Image): изображение со всеми тайлами.
    """

    tiles: list[list[int]] = field(default_factory=list)
    tile_size: int = 50

    def pos_to_tile(self, position: Vector2) -> Vector2:
        """Конвертирует локальную позицию в тайл."""
        return position // self.tile_size

    def tile_to_pos(self, tile: Vector2) -> Vector2:
        """Конвертирует тайл в локальную позицию."""
        return tile * self.tile_size

    def set_tile(self, row: int, col: int, tile_idx: int):
        """Устанавливает тайл по тайлсету."""
        self.tiles[row][col] = tile_idx

    def get_tile(self, row: int, col: int) -> int:
        """Возвращает тип тайла по тайлсету."""
        return self.tiles[row][col]


@dataclass
class TileMapController(Controller):
    """Контроллер карты тайлов. Считывает нажатия на тайлы карты."""

    on_tile_click: Event = field(default_factory=lambda: Event())

    def __post_init__(self):
        self.cursor.on_left_click.subscribe(self.on_left_click)

    def on_left_click(self, cursor):
        clicked_tile = self.model.pos_to_tile(cursor.global_pos)
        # print(f"Clicked tile: {self.model.pos_to_tile(cursor.global_pos)}")
        self.on_tile_click.emit(clicked_tile, self.model.tile_to_pos(clicked_tile))
