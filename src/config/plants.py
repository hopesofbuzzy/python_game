from pygame.math import Vector2

from src.core.objects.components.collision import RectShape

PLANTS = {
    0: None,
    1: "Mushroom",
    2: "Sunflower",
}

PLANTS_PRICES = {
    "Mushroom": 50,
    "Sunflower": 50
}

PLANTS_LEVEL_UPS = {
    "Sunflower": {"plant_name": "", "cost": 50000},
    "Mushroom": {"plant_name": "LongMushroom", "cost": 50},
    "LongMushroom": {"plant_name": "BigMushroom", "cost": 50},
    "BigMushroom": {"plant_name": "", "cost": 50000}
}

PLANTS_DESCRIPTIONS = {
    "Sunflower": str(
        "Подсолнышко\n"
        "Класс: дорожное растение\n"
        "Скорость: 5 подсолнышек / 10 сек\n"
        "Следующее улучшение: нет\n"
    ),
    "Mushroom": str(
        "Грибочек\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 0.7 сек\n"
        "Атака: 3 ед / 1 пуля\n"
        "Следующее улучшение: ВысокоГрибка\n"
        "(50 солнышек)"
    ),
    "LongMushroom": str(
        "ВысокоГрибка\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 0.25 сек\n"
        "Атака: 1 ед / 1 пуля\n"
        "Следующее улучшение: Большой гриб\n"
        "(50 солнышек)"
    ),
    "BigMushroom": str(
        "Большой гриб\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 1 сек\n"
        "Атака: 12 ед / 1 пуля\n"
        "Следующее улучшение: Нет\n"
    ),
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
                    position=Vector2(0, 0),
                    size=Vector2(50, 50), 
                    centred=True)
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
                "range":2,
                "speed": 150
            },
        ],
        "image_path": "res/mushroom.png",
    },
    "LongMushroom": {
        "components": [
            {
                "type":
                "targeting",
                "damage": 1,
                "cooldown": 0.25,
                "range": 4,
                "speed": 300
            },
        ],
        "image_path": "res/sunflower.png",
    },
    "BigMushroom": {
        "components": [
            {
                "type": "targeting",
                "damage": 12,
                "cooldown": 1,
                "range": 3,
                "speed": 200
            },
        ],
        "image_path": "res/mushroom.png",
    }
}

# Растения
PLANT_SIZE = Vector2(50, 50)
PLANT_HITBOX_SIZE = Vector2(25, 25)
PLANT_HITBOX_POSITION = PLANT_SIZE // 2
