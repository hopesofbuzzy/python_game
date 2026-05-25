import pygame
from pygame.event import Event
from pygame.math import Vector2
from dataclasses import dataclass, field
from pathlib import Path

from src.core.objects import *
from src.core.systems.images import Image
from src.core.systems.event import Event

@dataclass
class TileMapView(View):
    _tileset: dict[int, pygame.Surface] = field(default_factory=dict)

    def draw(self, screen: pygame.Surface, model, local_position):
        pos = local_position
        for ridx, row in enumerate(model._tiles):
            for cidx, tile_idx in enumerate(row):
                tile = self._tileset[tile_idx]
                screen.blit(tile, dest=(
                    pos.x + ridx * model.tile_size, pos.y + cidx * model.tile_size
                ))

@dataclass
class TileMapModel(Model):
    """
    Модель карты тайлов.

    Args:
        tiles (list[list[int]]): подгруженная карта.
        tileset (Image): изображение со всеми тайлами.
    """
    _tiles: list[list[int]] = field(default_factory=list)
    
    original_tile_size: int = 200
    tile_size: int = 50

    def pos_to_tile(self, position: Vector2) -> Vector2:
        """Конвертирует глобальную позицию в тайл."""
        return position // self.tile_size

    def tile_to_pos(self, tile: Vector2) -> Vector2:
        """Конвертирует тайл в глобальную позицию."""
        return tile * self.tile_size

    def set_tile(self, row: int, col: int, tile_idx: int):
        self._tiles[row][col] = tile_idx

@dataclass
class TileMapController(Controller):
    """Контроллер карты тайлов. Считывает нажатия на тайлы карты."""
    on_tile_click: Event = field(default_factory=lambda: Event())

    def on_left_click(self, cursor):
        clicked_tile = self.model.pos_to_tile(cursor.global_pos)
        # print(f"Clicked tile: {self.model.pos_to_tile(cursor.global_pos)}")
        self.on_tile_click.emit(clicked_tile, self.model.tile_to_pos(clicked_tile))