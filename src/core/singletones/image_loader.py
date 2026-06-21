import logging
from dataclasses import dataclass

import pygame


@dataclass
class Image:
    filename: str
    surface: pygame.Surface


class ImageLoader:
    """Регистр изображений для переиспользования."""

    def __init__(self):
        self.image_registry: dict[str, Image] = {}

    def load_image(self, filename: str) -> Image:
        """Подгрузка изображения из filename."""
        if filename not in self.image_registry:
            try:
                image = pygame.image.load(filename)
                self.image_registry[filename] = Image(filename, image)
            except Exception:
                logging.warning(f"Не удалось найти файл {filename}")
        return self.image_registry[filename]

    def cleanup(self):
        """Очистка регистра."""
        self.image_registry = {}


# Инициализируем ОДИН раз при импорте этого модуля
image_loader = ImageLoader()
