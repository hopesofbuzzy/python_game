from dataclasses import dataclass


@dataclass
class DataComponent:
    """Компонент данных сущности (растения)."""
    name: str
    tile_pos: tuple[int, int]
