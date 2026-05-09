import pygame
from dataclasses import dataclass

@dataclass
class Image:
    filename: str
    surface: pygame.Surface

class ImageLoader:
    """Регистр подгрузки изображения для переиспользования."""
    def __init__(self):
        self.image_registry: dict[str, Image] = {}

    def load_image(self, filename: str) -> Image:
        if not filename in self.image_registry:
            try:
                image = pygame.image.load(filename)
                self.image_registry[filename] = Image(filename, image)
            except Exception as e:
                raise FileNotFoundError(f"Не удалось найти файл {filename}")
        return self.image_registry[filename]

    def cleanup(self):
        self.image_registry = {}