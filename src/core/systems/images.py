import pygame
from dataclasses import dataclass

@dataclass
class Image:
    filename: str
    surface: pygame.Surface
    refcount: int = 1

class ImageLoader:
    """Регистр подгрузки изображения для переиспользования."""
    def __init__(self):
        self.image_registry: dict[str, Image] = {}

    def load_image(self, filename: str) -> Image:
        if filename in self.image_registry:
            self.image_registry[filename].refcount += 1
        else:
            try:
                image = pygame.image.load(filename)
                self.image_registry[filename] = Image(filename, image)
            except Exception as e:
                raise FileNotFoundError(f"Не удалось найти файл {filename}")
        return self.image_registry[filename]