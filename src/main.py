import pygame

from src.core.game import Game
from src.scenes.test import TestScene


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    game = Game(TestScene)
    delta_time = 0.0

    while game.running:
        game.update(delta_time)
        game.draw(screen)
        pygame.display.update()
        delta_time = clock.tick(60) / 1000.0

    pygame.quit()