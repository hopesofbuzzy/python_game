import pygame

class InputManager:
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False