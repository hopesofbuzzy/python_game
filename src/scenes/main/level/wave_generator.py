import math
import random

from src.scenes.main.systems.waves import Wave, WaveObject, ParsedWaves
from src.config.enemies import (
    BASE_WAVE_BUDGET,
    MINIMUM_WAVE_PAUSE,
    FIRST_WAVE_TIMESTAMP,
    START_WAVE_PAUSE,
    ENEMY_UNLOCK_WAVE,
    ENEMY_DATA
)

class WaveGenerator:
    def __init__(self):
        ...

    def generate_waves(self, count: int, seed=0):
        rng = random.Random(seed)
        waves = list()
        timestamp = FIRST_WAVE_TIMESTAMP
        for wave_number in range(1, count + 1):
            wave_budget = self.get_wave_budget(wave_number)
            possible_enemies = [
                enemy
                for enemy, unlock_wave in ENEMY_UNLOCK_WAVE.items()
                if wave_number >= unlock_wave
            ]
            rng.shuffle(possible_enemies)
            pos_enemies_count = len(possible_enemies)
            wave_objects = list()
            while wave_budget >= 100:
                for enemy in possible_enemies:
                    cost = ENEMY_DATA[enemy]["price"]
                    print(cost, wave_budget)
                    if wave_budget >= cost:
                        amount = wave_budget // cost
                        wave_object = WaveObject(enemy, amount)
                        wave_objects.append(wave_object)
                        print(wave_budget)
                        wave_budget -= cost * amount
                    pos_enemies_count -= 1
            wave = Wave(timestamp, wave_objects)
            waves.append(wave)
            timestamp += self.get_wave_puase(wave_number)
        return ParsedWaves(waves)

    def get_wave_budget(self, wave_number: int, base: int = BASE_WAVE_BUDGET):
        """Функция вычисления бюджета для спавна врагов на волну."""
        return base * (1.3 ** (wave_number + 2))

    def get_wave_puase(self, wave_number: int, minimum: int = MINIMUM_WAVE_PAUSE):
        """Высчитывает паузу перед следующей волной."""
        return max(minimum, START_WAVE_PAUSE - wave_number)