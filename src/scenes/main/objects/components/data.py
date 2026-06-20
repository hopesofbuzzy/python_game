from dataclasses import dataclass


@dataclass
class DataComponent:
    name: str
    tile_pos: tuple[int, int]