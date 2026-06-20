import json
from dataclasses import dataclass
from pathlib import Path

from src.core.singletones.image_loader import image_loader as il


def serialize_waves(parsed_waves):
    """Сериализация спарсенных волн (при генерции уровня)."""
    waves_list: list[dict] = list()
    for wave in parsed_waves.waves:
        wave_dict = {
            "timestamp": wave.timestamp,
            "enemy_type": [],
            "enemy_amount": []
        }
        for wave_object in wave.wave_objects:
            wave_dict["enemy_type"].append(wave_object.enemy)
            wave_dict["enemy_amount"].append(wave_object.amount)
        waves_list.append(wave_dict)
    return waves_list

class LevelSaver:
    """Сохранение (сгенерированного) уровня."""

    LEVELS_FOLDER = "res/levels/"
    TILESET_FOLDER = LEVELS_FOLDER + "tilesets/"
    MAPS_FOLDER = LEVELS_FOLDER + "maps/"

    def save_data(self, metadata: dict, level_name):
        """Сохранение данных."""
        with open(Path(self.LEVELS_FOLDER, f"{level_name}.json"), "w") as f:
            json.dump(metadata, f)

    def save_map(self, tiles: list, map_name):
        """Сохранение карты."""
        lines = list()
        for tile_line in tiles:
            lines.append(",".join(map(str, tile_line)))
        with open(Path(self.MAPS_FOLDER, f"{map_name}.csv"), "w") as f:
            for line in lines:
                f.write(line + "\n")

    def save_level(
            self,
            raw_level,
            parsed_waves,
            level_name: str
    ):
        """Сохранение уровня."""
        raw_level.metadata["map_name"] = level_name + ".csv"
        raw_level.metadata["waves"] = serialize_waves(parsed_waves)
        self.save_data(raw_level.metadata, level_name)
        self.save_map(raw_level.tiles, level_name)
