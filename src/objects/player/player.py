import pygame
from pygame.event import Event as PygameEvent
from dataclasses import dataclass

from src.core.objects import KinematicBodyModel, RectView, Controller

class PlayerModel(KinematicBodyModel):
    ...

@dataclass
class PlayerController(Controller):
    KEYS = {
        "up": (pygame.K_UP, pygame.K_w),
        "down": (pygame.K_DOWN, pygame.K_s),
        "left": (pygame.K_LEFT, pygame.K_a),
        "right": (pygame.K_RIGHT, pygame.K_d)
    }

    def handle_input(self, event: PygameEvent):
        keys = pygame.key.get_pressed()
        dx = self.direction("right", keys) - self.direction("left", keys)
        dy = self.direction("down", keys) - self.direction("up", keys)
        self.model.set_velocity(dx, dy)

    def direction(self, direction: str, keys):
        return int(any(keys[key] for key in self.KEYS[direction]))