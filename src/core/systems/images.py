from dataclasses import dataclass

import pygame


@dataclass
class Image:
    filename: str
    surface: pygame.Surface | None

class ImageLoader:
    """Регистр подгрузки изображения для переиспользования."""
    def __init__(self):
        self.image_registry: dict[str, Image] = {}

    def load_image(self, filename: str) -> Image:
        if filename not in self.image_registry:
            try:
                image = pygame.image.load(filename)
                self.image_registry[filename] = Image(filename, image)
            except Exception:
                raise FileNotFoundError(f"Не удалось найти файл {filename}")
        return self.image_registry[filename]

    def cleanup(self):
        self.image_registry = {}