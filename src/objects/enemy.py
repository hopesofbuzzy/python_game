import pygame
from pygame.event import Event as PygameEvent
from dataclasses import dataclass

from src.core.objects.collidable import Collidable
from src.core.objects import *

@dataclass
class EnemyModel(KinematicBodyModel):
    def handle_collision(self, other: Collidable):
        ...