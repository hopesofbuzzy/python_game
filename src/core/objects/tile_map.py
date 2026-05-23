import pygame
from pygame.math import Vector2
from dataclasses import dataclass, field
from pathlib import Path

from src.core.objects import View, Model
from src.core.systems.images import Image

@dataclass
class TileMapView(View):
    def draw(self, screen: pygame.Surface, model, local_position):
        pos = local_position
        for ridx, row in enumerate(model._tiles):
            for cidx, tile_idx in enumerate(row):
                tile = model._tileset[tile_idx]
                screen.blit(tile, dest=(
                    pos.x + ridx * model.tile_size, pos.y + cidx * model.tile_size
                ))

@dataclass
class TileMapModel(Model):
    """
    Args:
        tiles (list[list[int]]): подгруженная карта.
        tileset (Image): изображение со всеми тайлами.
    """
    tiles_path: Path
    tileset: Image
    _tiles: list[list[int]] = field(default_factory=list)
    _tileset: dict[int, pygame.Surface] = field(default_factory=dict)
    original_tile_size: int = 200
    tile_size: int = 40

    def __post_init__(self):
        # Загружаем уровень.
        with open(self.tiles_path, "r") as f:
            for line in f.readlines():
                self._tiles.append(list(map(int, line.split(","))))
        # Делим tileset, извлекая наши тайлы.
        surface = self.tileset.surface
        if surface:
            tileset_size = surface.get_size()
            original_tile_size = self.original_tile_size
            tile_size = self.tile_size
            tile_idx = 0
            for col in range(0, tileset_size[0], original_tile_size):
                for row in range(0, tileset_size[1], original_tile_size):
                    tile = surface.subsurface(
                        pygame.Rect(
                            (row, col), (
                                original_tile_size,
                                original_tile_size
                            )
                        )
                    )
                    tile = pygame.transform.scale(
                        tile,
                        size=(tile_size, tile_size)
                    )
                    self._tileset[tile_idx] = tile
                    tile_idx += 1