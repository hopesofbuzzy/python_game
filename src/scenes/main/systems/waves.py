import logging
from collections.abc import Callable
from dataclasses import dataclass
from random import randrange

from src.core.singletones.event_bus import EventBus, EventFlow

SPAWN_COOLDOWN = 0.5


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

    def __init__(
        self,
        parsed_waves: ParsedWaves,
        create_enemy_func: Callable,
        path,
        event_bus: EventBus,
    ):
        self.waves: list[Wave] = parsed_waves.waves
        self.create_enemy: Callable = create_enemy_func
        self._spawn_timer: float = SPAWN_COOLDOWN
        self.path = path
        self._time: float = 0.0
        # Состояние
        self.current_wave: Wave | None = None
        self.next_wave: Wave | None = None
        # Числовая статистика
        self.current_wave_number = 0
        self.time_before_next_wave = self.waves[0].timestamp
        # События
        self.event_bus = event_bus
        event_bus.subscribe("on_enemy_deleted", self.on_enemy_deleted)
        logging.debug(self.waves)

    def update(self, delta_time):
        self._time += delta_time
        self.time_before_next_wave -= delta_time
        if not self.process_wave(delta_time):
            for idx, wave in enumerate(self.waves):
                if self._time > wave.timestamp:
                    next_wave = None
                    if idx + 1 < len(self.waves):
                        next_wave = self.waves[idx + 1]
                    self.start_wave(wave)
                    if next_wave:
                        self.time_before_next_wave = (
                            next_wave.timestamp - self._time
                        )
                    else:
                        self.time_before_next_wave = -1
                    logging.info("Волна монстров!")

    def on_enemy_deleted(self, _event: EventFlow, enemy_count: int):
        logging.info(f"{len(self.waves)} {enemy_count}")
        if (len(self.waves) <= 1) and (enemy_count == 0):
            self.event_bus.fire("on_win")

    def start_wave(self, wave):
        """Старт волны."""
        self.current_wave = wave
        self.current_wave_number += 1
        self.event_bus.fire("on_wave_started", self.current_wave_number)

    def get_time_before_wave(self):
        """Время перед следующей волной."""
        return round(self.time_before_next_wave, 0)

    def process_wave(self, delta_time):
        """Обработка текущей волны."""
        if self.current_wave:
            # Пауза при спавне врагов.
            self._spawn_timer -= delta_time
            if self._spawn_timer < 0.0:
                self._spawn_timer = SPAWN_COOLDOWN
                wave_objects = self.current_wave.wave_objects
                rand_wave_obj_idx = randrange(0, len(wave_objects))
                wave_object = wave_objects[rand_wave_obj_idx]
                wave_object.amount -= 1
                # Спавн врага.
                self.event_bus.fire(
                    "on_enemy_spawn", wave_object.enemy, self.path
                )
                if wave_object.amount <= 0:
                    wave_objects.remove(wave_object)
                    if len(wave_objects) == 0:
                        self.waves.remove(self.current_wave)
                        self.current_wave = None
                        self._spawn_timer = SPAWN_COOLDOWN
            return True

    def get_wave_count(self):
        """Возвращает текущую волну."""
        return self.current_wave_number
