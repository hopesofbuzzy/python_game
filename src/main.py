import logging

import pygame

from src.core.game import Game
from src.scenes.menu.menu import MenuScene

# Логирование
logging.basicConfig(
    level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s"
)

# Глобальное состояние.
DEBUG = False
WINDOW_SIZE = (720, 720)


def main(scene_class):
    """
    Вход приложения.

    Args:
        scene_class: класс сцены инициализации.
    """
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    game = Game(scene_class, WINDOW_SIZE, debug=DEBUG)

    clock = pygame.time.Clock()
    delta_time = 0.0

    while game.running:
        game.update(delta_time)
        game.draw(screen)
        pygame.display.update()
        delta_time = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    main(MenuScene)
