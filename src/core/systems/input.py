import pygame

from src.core.systems.event import Event

class InputManager:
    def __init__(self):
        self.on_exit = Event()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_exit.emit()