import logging
from dataclasses import dataclass, field
from random import randrange
from typing import Callable

from pygame.math import Vector2

from src.scenes.main.objects.enemy import EnemyModel, EnemyView, FastEnemyModel, FastEnemyView
from src.core.systems.event import Event

ENEMIES = {
    "Enemy": (EnemyModel, EnemyView),
    "FastEnemy": (FastEnemyModel, FastEnemyView)
}
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
            create_enemy(cls_model, cls_view, position, path),
            path: PathModel
    """
    def __init__(self, parsed_waves: ParsedWaves, create_enemy: Callable, path):
        self._time: float = 0.0
        self.current_wave: Wave | None = None
        self.waves: list[Wave] = parsed_waves.waves
        self.create_enemy: Callable = create_enemy
        self._spawn_timer: float = SPAWN_COOLDOWN
        self.on_enemy_reach_end: Event = Event()
        self.path = path
        logging.debug(self.waves)

    def update(self, delta_time):
        self._time += delta_time
        if not self.process_wave(delta_time):
            for wave in self.waves:
                if self._time > wave.timestamp:
                    self.current_wave = wave
                    logging.info(f"Волна монстров!")

    def process_wave(self, delta_time):
        if self.current_wave:
            self._spawn_timer -= delta_time
            if self._spawn_timer < 0.0:
                self._spawn_timer = SPAWN_COOLDOWN
                wave_objects = self.current_wave.wave_objects
                rand_wave_obj_idx = randrange(0, len(wave_objects))
                wave_object = wave_objects[rand_wave_obj_idx]
                wave_object.amount -= 1
                enemy_cls_model, enemy_cls_view = ENEMIES[wave_object.enemy]
                enemy = self.create_enemy(
                    enemy_cls_model,
                    enemy_cls_view,
                    Vector2(200, 200),
                    self.path
                )
                enemy.model.on_reach_end.subscribe(lambda: self.on_enemy_reach_end.emit())
                if wave_object.amount <= 0:
                    wave_objects.remove(wave_object)
                    if len(wave_objects) == 0:
                        self.waves.remove(self.current_wave)
                        self.current_wave = None
                        self._spawn_timer = SPAWN_COOLDOWN
            return True
