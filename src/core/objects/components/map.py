import logging

import pygame
from pygame.event import Event
from pygame.math import Vector2

from src.core.objects.event import Event
from src.core.objects.game_object import GameObject
from src.core.singletones.event_bus import EventFlow, event_bus


class MapViewComponent:
    def __init__(
        self,
        map_model,
        tileset: dict[int, pygame.Surface],
        tile_size: int = 50
    ):
        self._scaled_tilesets: dict[float, dict] = dict()
        self.map_model = map_model
        self.tileset = tileset
        self.tile_size = tile_size



    def get_scaled_tileset(self, size: float):
        """Кэширование тайлов для зума камеры."""
        if size not in self._scaled_tilesets.keys():
            self._scaled_tilesets[size] = dict()
            for tile_idx, tile in self.tileset.items():
                overall_size = (self.tile_size * size, self.tile_size * size)
                tile = pygame.transform.scale(tile, size=overall_size).convert()
                self._scaled_tilesets[size][tile_idx] = tile
        return self._scaled_tilesets[size]

    def draw(self, screen: pygame.Surface, size, local_position, camera):
        pos = local_position
        scaled_tileset = self.get_scaled_tileset(camera.zoom)
        c1, c2, r1, r2 = camera.get_visible_range(
            self.tile_size,
            len(self.map_model.tiles[0]) + 1,
            len(self.map_model.tiles) + 1
        )
        for row in range(r1, r2):
            for col in range(c1, c2):
                tile = scaled_tileset[self.map_model.tiles[row][col]]
                screen.blit(
                    tile,
                    dest=(
                        pos.x + col * self.map_model.tile_size * camera.zoom,
                        pos.y + row * self.map_model.tile_size * camera.zoom,
                    ),
                )


class MapModelComponent:
    """
        Модель карты тайлов.

        Args:
            tiles (list[list[int]]): подгруженная карта.
            tileset (Image): изображение со всеми тайлами.
    """
    def __init__(self, tiles: list[list[int]], tile_size: int = 50):
        self.tiles = tiles
        self.tile_size = tile_size

    def pos_to_tile(self, position: Vector2) -> Vector2:
        """Конвертирует локальную позицию в тайл."""
        return position // self.tile_size

    def tile_to_pos(self, tile: Vector2) -> Vector2:
        """Конвертирует тайл в локальную позицию."""
        return tile * self.tile_size

    def tile_to_pos_centred(self, tile: Vector2) -> Vector2:
        """Конвертирует тайл в локальную позицию по центру тайла."""
        return tile * self.tile_size + Vector2(1, 1) * self.tile_size // 2

    def set_tile(self, row: int, col: int, tile_idx: int):
        """Устанавливает тайл по тайлсету."""
        self.tiles[row][col] = tile_idx

    def is_tile_valid(self, row: int, col: int):
        return row in range(0, len(self.tiles)) and col in range(0, len(self.tiles[0]))

    def get_tile(self, row: int, col: int) -> int:
        """Возвращает тип тайла по тайлсету."""
        if self.is_tile_valid(row, col):
            return self.tiles[row][col]
        else:
            return -1


class MapControllerComponent:
    """
        Контроллер карты тайлов. Считывает нажатия на тайлы карты.

        Args:
        on_tile_click(tile_pos: Vector2, tile_type: int, global_pos)
    """
    def __init__(self, map_model: MapModelComponent):
        self.map_model = map_model
        self.on_tile_click: Event = Event()
        event_bus.subscribe("on_mouse_left_click", self.on_mouse_left_click)

    def on_mouse_left_click(self, event: EventFlow, cursor):
        tile_pos = self.map_model.pos_to_tile(cursor.global_pos)
        global_pos_centred = self.map_model.tile_to_pos_centred(tile_pos)
        tile_type = self.map_model.get_tile(int(tile_pos.y), int(tile_pos.x))
        self.on_tile_click.emit(
            event,
            tile_pos,
            global_pos_centred,
            tile_type,
            self.map_model.tile_to_pos(tile_pos)
        )


class Map(GameObject):
    def __init__(self):
        super().__init__()