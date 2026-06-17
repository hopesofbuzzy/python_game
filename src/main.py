import logging

import pygame

from src.core.game import Game
from src.scenes.main.main import MainScene

logging.basicConfig(
    level=logging.DEBUG,
    format='%(filename)s - %(levelname)s - %(message)s'
)

DEBUG = False

def main(scene_class):
    pygame.init()
    game = Game(scene_class, debug=DEBUG)
    screen = pygame.display.set_mode(game.WINDOW_SIZE)
    clock = pygame.time.Clock()
    delta_time = 0.0

    while game.running:
        game.update(delta_time)
        game.draw(screen)
        pygame.display.update()
        delta_time = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    main(MainScene)
