import pygame
import asyncio

from src.core.game import Game
from src.scenes.test import TestScene


async def main():
    pygame.init()
    game = Game(TestScene)
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
    asyncio.run(main())
