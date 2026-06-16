import logging
from dataclasses import dataclass, field
from random import randrange
from typing import Callable

from pygame.math import Vector2

from src.core.objects.components.path import PatrolComponent
from src.core.objects.event import Event

SPAWN_COOLDOWN = 1.0

@dataclass
class WaveObject:
    """Отдельный объект волны с типом врага и его коичеством."""
    enemy: str
    amount: int

@dataclass
class Wave:
    """Волна, содержащая объекты волны, с меткой о времени начала."""
    timestamp: float
    wave_objects: list[WaveObject]

@dataclass
class ParsedWaves:
    """Обработанный лист волн."""
    waves: list[Wave]

class WaveManager:
    """
        Управляет волнами монстров.

        Инъекции:
            parsed_waves
            create_enemy,
            path: PathComponent
    """
    def __init__(self, parsed_waves: ParsedWaves, create_enemy_агтс: Callable, path):
        self._time: float = 0.0
        self.current_wave: Wave | None = None
        self.waves: list[Wave] = parsed_waves.waves
        self.create_enemy: Callable = create_enemy_агтс
        self._spawn_timer: float = SPAWN_COOLDOWN
        self.on_enemy_reached_end: Event = Event()
        self.path = path
        # Статистика
        self.current_wave_number = 0
        logging.debug(self.waves)

    def update(self, delta_time):
        self._time += delta_time
        if not self.process_wave(delta_time):
            for wave in self.waves:
                if self._time > wave.timestamp:
                    self.start_wave(wave)
                    logging.info(f"Волна монстров!")

    def start_wave(self, wave):
        self.current_wave = wave
        self.current_wave_number += 1

    def process_wave(self, delta_time):
        if self.current_wave:
            self._spawn_timer -= delta_time
            if self._spawn_timer < 0.0:
                self._spawn_timer = SPAWN_COOLDOWN
                wave_objects = self.current_wave.wave_objects
                rand_wave_obj_idx = randrange(0, len(wave_objects))
                wave_object = wave_objects[rand_wave_obj_idx]
                wave_object.amount -= 1
                enemy = self.create_enemy(
                    wave_object.enemy,
                    Vector2(200, 200),
                    self.path
                )
                enemy.get(PatrolComponent).on_reached_end.subscribe(
                    lambda: self.on_enemy_reached_end.emit()
                )
                if wave_object.amount <= 0:
                    wave_objects.remove(wave_object)
                    if len(wave_objects) == 0:
                        self.waves.remove(self.current_wave)
                        self.current_wave = None
                        self._spawn_timer = SPAWN_COOLDOWN
            return True
