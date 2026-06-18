from pygame.math import Vector2

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
    ),
    "LongMushroom": str(
        "ВысокоГрибка\n"
        "Класс: травяное растение\n"
        "Скорость: 1 пуля / 0.25 сек\n"
        "Атака: 1 ед / 1 пуля\n"
        "Следующее улучшение: Большой гриб\n"
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
        "targeting": False,
        "cooldown": 10,
        "image_path": "res/sunflower.png",
        "health": 15,
        "given_sun": 25
    },
    "Mushroom": {
        "road_spawn": False,
        "targeting": True,
        "attack": 2,
        "cooldown": 0.7,
        "image_path": "res/mushroom.png",
        "range": 2,
        "bullet_speed": 150
    },
    "LongMushroom": {
        "targeting": True,
        "attack": 1,
        "cooldown": 0.25,
        "image_path": "res/sunflower.png",
        "range": 4,
        "bullet_speed": 300
    },
    "BigMushroom": {
        "targeting": True,
        "attack": 12,
        "cooldown": 1,
        "image_path": "res/mushroom.png",
        "range": 3,
        "bullet_speed": 200
    }
}

# Растения
PLANT_SIZE = Vector2(50, 50)
PLANT_HITBOX_SIZE = Vector2(25, 25)
PLANT_HITBOX_POSITION = PLANT_SIZE // 2
