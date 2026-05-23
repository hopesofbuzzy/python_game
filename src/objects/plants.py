from dataclasses import dataclass, field

from src.core.objects import *

@dataclass
class PlantModel(Model):
    """Универсальное растение."""
    ...

@dataclass
class ShooterModel(PlantModel):
    """Растение, стреляющее во врагов на дистанции."""
    range: int = 100

    def handle_targets(self, targets: list):
        print(self, len(targets))

@dataclass
class MushroomModel(ShooterModel):
    """Грибок-стрелок."""
    ...