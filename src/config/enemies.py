from pygame.math import Vector2

ENEMY_DATA = {
    "Enemy": {
        "price": 300,
        "speed": 10,
        "health": 100,
        "size": Vector2(40, 40),
        "color": (255, 25, 25),
        "attack": 5,
        "attack_cooldown": 0.5,
    },
    "FastEnemy": {
        "price": 100,
        "speed": 25,
        "health": 25,
        "size": Vector2(30, 30),
        "color": (80, 80, 255),
        "attack": 5,
        "attack_cooldown": 0.5,
    },
    "Minion": {
        "price": 20,
        "speed": 50,
        "health": 5,
        "size": Vector2(20, 20),
        "color": (80, 255, 80),
        "attack": 1,
        "attack_cooldown": 0.5,
    },
}

ENEMY_UNLOCK_WAVE = {"FastEnemy": 1, "Enemy": 2, "Minion": 1}

BASE_WAVE_BUDGET = 100
MINIMUM_WAVE_PAUSE = 20
START_WAVE_PAUSE = 30
FIRST_WAVE_TIMESTAMP = 20
