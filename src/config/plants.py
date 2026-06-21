from pygame.math import Vector2

from src.core.objects.components.collision import RectShape

PLANTS = {
    0: None,
    1: "Mushroom",
    2: "Sunflower",
}

PLANTS_PRICES = {"Mushroom": 50, "Sunflower": 50}

PLANTS_LEVEL_UPS = {
    "Sunflower": {"plant_name": "", "cost": 50000},
    "Mushroom": {"plant_name": "LongMushroom", "cost": 50},
    "LongMushroom": {"plant_name": "BigMushroom", "cost": 50},
    "BigMushroom": {"plant_name": "", "cost": 50000},
}

PLANTS_DESCRIPTIONS = {
    "Sunflower": (
        "Подсолнышко\n"
        "Выдаёт СОЛНЫШКИ\n"
        "Класс: дорожное растение\n"
        "Частота: 10 сек\n"
    ),
    "Mushroom": (
        "Грибочек\n"
        "Стреляет по врагам\n"
        "Класс: травяное растение\n"
        "Частота 0.7 сек\n"
        "Урон: 3\n"
    ),
}

PLANTS_UPGRADE_DESCRIPTIONS = {
    "Sunflower": "Подсолнышко (Максимум)\n" "Частота: 10 сек\n",
    "Mushroom": (
        "Грибочек -> ВысокоГрибка\n"
        "Частота: 0.7 -> 0.25 (сек)\n"
        "Урон: 3 -> 1\n"
        "(50 солнышек)"
    ),
    "LongMushroom": (
        "ВысокоГрибка -> Большой гриб\n"
        "Частота: 0.25 -> 1 (сек)\n"
        "Урон: 1 -> 12\n"
        "(50 солнышек)"
    ),
    "BigMushroom": "Большой гриб (Максимум)\n"
    "Частота: 1 (сек)\n"
    "Урон: 12\n",
}

PLANT_DATA = {
    "Sunflower": {
        "road_spawn": True,
        "components": [
            {"type": "cycle_timer", "time": 10, "data": 15},
            {"type": "health", "hp": 15},
            {
                "type": "collision",
                "shape": RectShape(
                    position=Vector2(0, 0), size=Vector2(50, 50), centred=True
                ),
            },
        ],
        "image_path": "res/sunflower.png",
    },
    "Mushroom": {
        "road_spawn": False,
        "components": [
            {
                "type": "targeting",
                "damage": 2,
                "cooldown": 0.7,
                "range": 2,
                "speed": 150,
            },
        ],
        "image_path": "res/mushroom.png",
    },
    "LongMushroom": {
        "components": [
            {
                "type": "targeting",
                "damage": 1,
                "cooldown": 0.25,
                "range": 4,
                "speed": 300,
            },
        ],
        "image_path": "res/long_mushroom.png",
    },
    "BigMushroom": {
        "components": [
            {
                "type": "targeting",
                "damage": 12,
                "cooldown": 1,
                "range": 3,
                "speed": 200,
            },
        ],
        "image_path": "res/big_mushroom.png",
    },
}

# Растения
DEFAULT_RANGE = 1
PLANT_SIZE = Vector2(50, 50)
PLANT_HITBOX_SIZE = Vector2(25, 25)
PLANT_HITBOX_POSITION = PLANT_SIZE // 2


def get_plant_range(plant_name: str) -> int:
    for comp in PLANT_DATA[plant_name]["components"]:
        if "range" in comp:
            return comp["range"]
    return DEFAULT_RANGE
