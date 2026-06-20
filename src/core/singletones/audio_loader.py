import logging
from dataclasses import dataclass

import pygame


@dataclass
class Sfx:
    filename: str
    sound: pygame.mixer.Sound


class AudioLoader:
    """Регистр подгрузки аудио для переиспользования."""

    def __init__(self):
        self.sfx_registry: dict[str, Sfx] = {}

    def load_music(self, filename: str):
        pygame.mixer.music.load(filename)

    def play_music(self, times: int):
        pygame.mixer.music.play(times)

    def load_sfx(self, filename: str) -> Sfx:
        if filename not in self.sfx_registry:
            try:
                sfx = pygame.mixer.Sound(filename)
                self.sfx_registry[filename] = Sfx(filename, sfx)
            except Exception:
                logging.warning(f"Не удалось найти файл {filename}")
        return self.sfx_registry[filename]

    def cleanup(self):
        self.sfx_registry = {}


# Инициализируем ОДИН раз при импорте этого модуля
audio_loader = AudioLoader()